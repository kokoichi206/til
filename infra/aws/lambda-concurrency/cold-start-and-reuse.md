# 実行環境の再利用とコールドスタート（調査メモ）

[README.md](./README.md) の並列性実験で使ったのと同じ関数・ログを材料に、
「2 回目以降の invocation はキャッシュに乗って速いのか」「そのキャッシュは
何単位なのか」を調べたメモ。

## 問い

1. Lambda の起動は重い（JVM の Spring Boot 等）。2 回目以降の invocation は
   初期化済みの状態を再利用して速くなるのか。
2. その「キャッシュ」は何の単位で効くのか（実行環境ごとか、グローバルに共有か）。

## 結論

1. 速くなる。ただし「キャッシュ」ではなく**実行環境の凍結(freeze)と解凍(thaw)による再利用**。
   handler の外（static 初期化 / Init フェーズ）で作った状態は、その実行環境が warm な間は
   再初期化されない。
2. 再利用の単位は**実行環境(env)ごと**。同時リクエストは別 env に振られるので env をまたいで
   共有されない。しかも再利用は保証ではなくベストエフォート（"where possible"）。

## 実測との対応（実行時間）

README の実験（各リクエスト 5 秒 sleep / 10 並列 / ap-northeast-1 / nodejs22.x）で観測した値。

| ランナー | reserved conc | 合計 | 異なる envId | 1env内 max inFlight |
|---|---|---|---|---|
| ローカル Node HTTP server | － | 5.04 s | 1 | 10 |
| lambda-plain | 1 | 52.38 s | 1 | 1 |
| lambda-plain | 10 | 5.49 s | 10 | 1 |
| lambda-lwa | 1 | 52.40 s | 1 | 1 |
| lambda-lwa | 10 | 5.54 s | 10 | 1 |

コールド/ウォームの内訳（同じ実験の生ログから）:

- 単発の疎通（コールド込み）: plain `http 200 in 5.53s` / lwa `5.71s`。
  handler 本体は 5 秒 sleep なので、超過分の **約 0.5〜0.7 秒が Init（コールドスタート）**。
- warm な各回の `durationMs` は一貫して **5006**（＝sleep 5000 + 誤差、初期化コスト 0）。
- concurrency=1 の env `f27830b8` は全 run を通じて `invocations` が 1→11→12 と増えたが、
  `durationMs` は毎回 5006。→ **同じ env が再利用され、2 回目以降は初期化を払っていない**。
- concurrency=10 の合計 5.49s のうち超過分 約 0.5s は、**新規 10 env が同時にコールドスタート**した分。

我々の Node 関数は Init が約 0.5 秒と軽いのでこの差は小さいが、**Spring Boot ならこの部分が
数秒**になる。そしてそれを払うのはコールドの 1 回だけで、warm な 2 回目以降は handler 実行だけになる。

## 仕組み: なぜ 2 回目が速いか

Lambda のライフサイクルは Init フェーズと Invoke フェーズに分かれる。

- Init フェーズ: ランタイム起動 + handler の外側の初期化コード（static initialization）を実行。
  JVM 起動・Spring ApplicationContext 構築・DB コネクション確立はここでやるのが定石。
- Invoke フェーズ: handler メソッドの実行。invocation ごとに毎回走る。

呼び出し後、env は凍結され、次の呼び出しで解凍して再利用される。このとき Init は再実行されない。

> "During this entire process, this execution environment is busy and cannot process other
> requests. When Lambda finishes processing the first request, this execution environment can
> then process additional requests for the same function. **For subsequent requests, Lambda
> doesn't need to re-initialize the environment.**"
> — [Understanding Lambda function scaling](https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html#understanding-concurrency)

> "When the function is invoked again, Lambda thaws the environment for reuse. **Reusing the
> execution environment has the following implications: Objects declared outside of the
> function's handler method remain initialized** ... if your Lambda function establishes a
> database connection, instead of reestablishing the connection, the original connection is
> used in subsequent invocations."
> — [execution environment lifecycle](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html#runtimes-lifecycle-shutdown)

## 「キャッシュは env 単位」の根拠

単一の文で「per-env cache」とは書かれていない。次の 3 記述の合成で導ける。

(A) 同じ env の再利用で初期化を省く（上記引用）。

(B) 同時リクエストは別 env に振られる:

> "**For each concurrent request, Lambda provisions a separate instance of your execution
> environment.**"
> — [同上 concurrency doc](https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html#understanding-concurrency)

(C) 単一 invocation 前提で、グローバル state に依存するな（＝実質 env ローカルの明文）:

> "For standard Lambda functions, **you should assume that the environment exists only for a
> single invocation.** ... It should not rely on any existing data structures or temporary
> files, or any internal state that would be managed by multiple invocations."

> "To initialize database connections and libraries, or load state, you can take advantage of
> static initialization. **Since execution environments are reused where possible** to improve
> performance, you can amortize the time taken to initialize these resources over multiple
> invocations. However, **you should not store any variables or data used in the function
> within this global scope.**"
> — [Implement statelessness in functions](https://docs.aws.amazon.com/lambda/latest/dg/concepts-application-design.html#statelessness-functions)

実験でグローバルの `ENV_ID`(UUID) が env ごとに別値・env 内で一定だったのは、この
「グローバル state は env ローカル」の実演。JVM/Spring の初期化済みコンテキストも同じ扱い。

補足: concurrency=10 で全 env の Node プロセス PID が同値だった（plain=2, lwa=5）。各 env は
独立した microVM でまっさらな名前空間から起動するため PID が被り、**PID は env 識別子にならない**。

## スケールアウト時の注意（並列性の話と直結）

キャッシュは env 単位なので、バーストで env が増えるとその**新規 env はそれぞれコールドスタート**する。

- concurrency=10 の実験で envId が 10 個に増えたとき、10 env は各々初期化を払っている。
- warm が速いのは「トラフィックが既存 env の再利用に収まっている間」だけ。
- 保証ではなくベストエフォート。アイドルが続く/数時間ごとに env は破棄され、その後はまたコールド。

## JVM / Spring のコールドを縮める手段

1. **SnapStart（Java など、追加課金なし）**: 初期化済み実行環境のスナップショットから復元する。
   JVM 起動 + Spring コンテキスト構築ごと凍結・復元するので Spring Boot のコールドに最も効く。
   > "Lambda saves a snapshot of the memory and disk state of the initialized execution
   > environment, persists the encrypted snapshot, and caches it for low-latency access."
   > — [execution environment lifecycle（Init/SnapStart）](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html#runtimes-lifecycle-ib)

   注意: スナップショットに状態が焼き付く。乱数シードの一意性や、コネクション再確立の
   runtime hook（after-restore）を要検討。
2. **Provisioned Concurrency（課金あり）**: N 個の env を事前初期化して常備。コールド自体を出さない。
3. **初期化を軽くする**: 使う依存だけ import、遅延ロード等。Init は 10 秒制限がある点も留意。

## 参考リンク

- Understanding Lambda function scaling: https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html
- Understanding the Lambda execution environment lifecycle: https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html
- Designing Lambda applications（statelessness）: https://docs.aws.amazon.com/lambda/latest/dg/concepts-application-design.html
- Lambda SnapStart: https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html
