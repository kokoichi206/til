# Lambda の並列性の単位を確かめる

関連: [実行環境の再利用とコールドスタート](./cold-start-and-reuse.md)（2 回目以降が速い理由・キャッシュの単位・SnapStart）

## 確かめたかったこと

Lambda は「I/O wait 中に同じ実行環境で別リクエストを処理する」のか、それとも
「I/O wait 中でも 1 invocation が実行環境を占有し、並列化は execution environment
の増加でしか起きない」のか。

観測する軸は 2 つだけ。

1. 同じ envId（実行環境）の中で inFlight が 2 以上になるか
2. 各リクエストが 5 秒待つだけの処理を 10 並列で投げたとき、合計時間が約 5 秒か約 50 秒か

## 結論

デフォルトの Lambda では、**1 つの実行環境は 1 invocation を処理中に他のリクエストを
受けない**。並列化は実行環境の増加でしか起きない。**Lambda Web Adapter を入れても
この単位は変わらない**（複数リクエストの同時処理は Lambda Managed Instances という別の
オプトイン機能の領分）。

一次情報:

- "During this entire process, this execution environment is busy and cannot
  process other requests." — [Understanding Lambda function scaling](https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html)
- "For each concurrent request, Lambda provisions a separate instance of your
  execution environment." — 同上
- Web Adapter は「Lambda の invoke イベント → ローカル HTTP server への 1 リクエスト」
  への変換ブリッジ。多重同時処理は "Lambda Managed Instances for multi-concurrent
  request handling" の役割 — [aws-lambda-web-adapter](https://github.com/awslabs/aws-lambda-web-adapter)

## 実測結果（ap-northeast-1 / nodejs22.x / 各リクエスト 5 秒 sleep / 10 並列）

| ランナー | reserved concurrency | 合計時間 | 異なる envId 数 | 1 env 内の最大 inFlight |
|---|---|---|---|---|
| ローカル Node HTTP server | － | 5.04 s | 1 | 10 |
| lambda-plain（普通の handler） | 1 | 52.38 s | 1 | 1 |
| lambda-plain | 10 | 5.49 s | 10 | 1 |
| lambda-lwa（Web Adapter + 同一 server） | 1 | 52.40 s | 1 | 1 |
| lambda-lwa | 10 | 5.54 s | 10 | 1 |

読み解き:

- ローカルの普通の HTTP server は 1 プロセス（envId 1 個）で 10 リクエストを
  I/O wait 中に多重処理する（maxInFlight=10）。だから合計 ~5 秒。
- Lambda は concurrency=1 だと 1 つの実行環境が 10 回**直列**に処理する
  （envId 1 個・maxInFlight=1・合計 ~50 秒）。I/O wait 中でも次を受けない。
- Lambda は concurrency=10 だと実行環境が 10 個に増え、各 env が 1 リクエストずつ
  処理する（envId 10 個・各 maxInFlight=1・合計 ~5 秒）。並列化の単位は実行環境。
- **lambda-lwa は lambda-plain と同じ挙動**。ローカルと同一の `src/server.mjs` を
  動かしているのに maxInFlight は 1 のまま。「Express を Lambda に載せたんだから
  I/O wait 中に多重処理されるはず」という直感は成り立たない。

補足: concurrency=10 の各 env は独立した microVM で、内部の Node プロセス PID は
どの env でも同じ値になる（plain=2, lwa=5）。そのため PID は実行環境の識別子に
ならない。モジュール初期化時に採番した UUID（`ENV_ID`）だけが実行環境ごとに一意。

## 構成

同一ロジック `work(sleepMs) = await sleep` を 3 ランナーで共有する。

```
src/shared.mjs   ENV_ID の採番と inFlight / maxInFlight / invocations の計測
src/lambda.mjs   普通の async handler（lambda-plain、Function URL 背後）
src/server.mjs   http server（ローカル基準 と lambda-lwa が同一ファイルを実行）
src/run.sh       Web Adapter の起動コマンド（Handler = run.sh）
driver/drive.mjs N 並列で叩き envId 単位で集計。throttle(429) はポーリング再試行
infra/           terraform（2 関数 + Function URL + reserved concurrency 変数）
build.sh         dist/plain.zip と dist/lwa.zip を生成（run.sh の実行ビットを保持）
```

lambda-lwa の要点（[公式サンプル](https://github.com/awslabs/aws-lambda-web-adapter/tree/main/examples/expressjs-zip) 準拠）:

- Layer `LambdaAdapterLayerX86:28`、`Handler = run.sh`、`AWS_LAMBDA_EXEC_WRAPPER=/opt/bootstrap`、`PORT=8000`
- readiness probe が計測を汚さないよう `AWS_LWA_READINESS_CHECK_PATH=/healthz` に分離し、
  `/healthz` は `work()` を呼ばず即 200 を返す

## 再現手順

```bash
# 依存: node, aws cli（認証済み）, terraform, zip

# 1. ローカル基準（普通の HTTP server）
./build.sh
SLEEP_MS=5000 PORT=8000 node src/server.mjs &
node driver/drive.mjs http://localhost:8000/ 10 "local"
kill %1

# 2. Lambda（concurrency=1 → 直列 ~50s）
cd infra && terraform init
terraform apply -auto-approve -var reserved_concurrency=1
node ../driver/drive.mjs "$(terraform output -raw plain_url)" 10 "plain conc=1"
node ../driver/drive.mjs "$(terraform output -raw lwa_url)"   10 "lwa conc=1"

# 3. Lambda（concurrency=10 → 並列 ~5s）
terraform apply -auto-approve -var reserved_concurrency=10
node ../driver/drive.mjs "$(terraform output -raw plain_url)" 10 "plain conc=10"
node ../driver/drive.mjs "$(terraform output -raw lwa_url)"   10 "lwa conc=10"

# 4. 後片付け（Function URL は auth=NONE の公開エンドポイントなので必ず削除）
terraform destroy -auto-approve -var reserved_concurrency=10
```

注意: Function URL を `authorization_type = NONE`（公開）で作る。URL を知る誰でも
呼び出せるので、実験が終わったら `terraform destroy` で必ず削除する。

## 補足: concurrency=1 で ~50s を出すための throttle 対応

同期呼び出し（Function URL / RequestResponse）は concurrency 上限を超えた分を
**キューせず 429 TooManyRequestsException で即返す**。10 並列を素で投げると
1 件成功・9 件即エラーで終わり ~50s にならない。`driver/drive.mjs` は 429 を受けたら
一定間隔でポーリング再試行し、空いた枠に順次入ることで直列 ~50s を再現している。
