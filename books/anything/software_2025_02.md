## なんでも

- Flatcar Container Linux
  - コンテナに最適化された OS
  - immutable なファイルシステム
- DNS security
  - BGP ハイジャック
  - SSL 証明書
    - DNS に攻撃を受けてドメインが偽装される場合 SSL 証明書で被害が防げるようになってる！？
- 自己実現
  - 人生の目標？
    - 他人軸で目標を作ってないか。。
  - **目標の前に目的があるべき**
    - 人生における目的の1つ
      - **自己実現**
    - 自分の価値観
    - 自分の人生観過去の出来事の棚卸し
      - その時の情景、相手がどのような表情だったか。。
- db
  - 範囲型, 複数範囲型
    - **時間枠の検索とかに適してそう！**
      - **これのためだけに postgresql の選定理由になりうる！**
    - tsrange
      - https://www.postgresql.jp/docs/9.4/functions-range.html
    - **ORM がサポートしていないケースでは View にしてから呼び出すなどの工夫が必要**
    - **範囲型の Index 指定には注意する！**
- software test
  - **仕様のサンプリング方法**
    - テスト技法
      - 境界値分析法
        - BVA: Boundary-Value Analysis
      - 同値分析法
        - ECP: Equivalence Class Partitioning
      - プロパティーベースドテスト
        - PBT: Property-Based Testing
  - BVA
    - 適している前提がある
    - On-Off ポイント法
      - 異なる処理が行われる、一番近い2つの値を選ぶ
    - 入力を人間が選ぶ
  - PBT
    - **入力が自動的に選ばれる**
    - 入力の生成方法？
      - 含意を使うアプローチ
      - ジェネレータを実装するアプローチ
    - js のライブラリ
      - fast-check
- 開発者体験
  - **ChatOps**
  - NewsPicks
    - **月 200-300 回のデプロイ**
      - 障害のほとんどはデプロイによって引き起こされる
    - **ポストモーテム**
  - 障害対応
    - **速やかに障害の暫定復旧をする**
    - **根本対策を検討するためにポストもーてむの開催判断をすること**
- AWS
  - Invoice Configuration
    - https://aws.amazon.com/jp/about-aws/whats-new/2024/12/aws-invoice-configuration/
- CDN
  - 事業者例
    - Akamai: AS 番号 20940
    - CloudFront: AS 番号 16509
    - Fastly: AS 番号 54113
    - Cloudflare: AS 番号 13335
  - **CDN の仕組みを独自開発**
    - Google, Netflix
  - Open Caching
    - ISP 内部に CDN キャッシュを置いて配信する仕組み
      - 小〜中規模のコンテンツ事業者にも利用できるようにした
    - https://voice.stream.co.jp/technology/20240307/
  - **インターネットトラフィック全体のうち 90% は CDN**
  - 技術広報
    - 

## Python

### basic

- 1 statement in 1 line
- 組み込み型
  - None オブジェクト
  - ビット演算子
    - `~`, `&`, `|`, `^`, `>>`, `<<`
  - ミュータブルとイミュータブル
    - リストはミュータブル
    - タプルはイミュータブル
  - **集合**
    - `set()` は**要素のない集合オブジェクト**を表す
    - 積集合
      - `{1, 2, 3} & {2, 3, 4}`
- デバッグ用 f 文字列
  - `f'{var=}'`
  - `f'{var+var2=}'`

**ジェネレータ式**

``` python
list1 = [1,2,3]
squares = (x**2 for x in list1 if x % 2 == 0)
sum(squares)
```

- `match-case`
  - 3.10 から使える

### データ構造

- `リスト内包表記の [] を () にするだけでジェネレータになる`
- 広く使われている Python の実態は C 言語
  - リストの実態は C 言語の配列
    - C 言語の配列は連続したメモリ領域
  - **内包表記はあらかじめ必要なメモリ領域を見積もることができる可能性があり append による計算負荷の低減・パフォーマンスの向上が見込める**
- namedtuple
  - タプルと同じようにデータを保持しつつ、それぞれのデータに名前でアクセスできる
- 辞書型のキーは重複が許されない
  - 同一とみなされるものは1つの値しか紐づけられない
    - 1, 1.0, True
- set and frozenset

### エラーと例外

- [エラーの種類](https://docs.python.org/ja/3.13/tutorial/errors.html)
  - 構文エラーと例外
    - syntax error and exception
  - **例外はエラーの一種**
    - c.f. Java
      - **エラー**
        - プログラムで捕捉できない重大な問題
      - **例外**
        - プログラムで対処可能な問題
- Linter
  - **Ruff**
    - 2022
    - 高速
    - Pylint, Flask8 と互換性あり

### 型ヒント

- カスタムジェネリック型
- **TypedDict**
- 型エイリアス
  - `type NewType = Union[int, float]`
  - `ReadOnly`
- 関数オブジェクト
  - **Callable**
- **Protocol**
  - **これ使いたい！！**

### コーディング規約

- pep8
  - https://pep8-ja.readthedocs.io/ja/latest/

### Links

- [Writing Clean Python With Namedtuples](https://dbader.org/blog/writing-clean-python-with-namedtuples)

## PostgreSQL 17

### basic

- 2024/09/26
- extension
  - Contrib modules
    - `pg_stat_statements`
    - `auto_explain`
    - `citext`
    - `fuzzystrmatch`
    - `pg_prewarm`
- **列指向テーブルとかも作れる！**
- PostgreSQL の特徴（ビジネス用 RDBMS としての特徴）
  - マルチプロセスアーキテクチャ
  - トランザクション分離レベル
  - 多彩なデータ型
    - `json`, `jsonb`
    - `xml`
    - `money`
    - `inet`
    - `point`, `line`, `lseg`, ...
    - `macaddr`
- メイン機能
  - レプリケーション
  - パラレルクエリ
    - SQL の実行
      - ⇨ クライアントと接続を担当する単一のバックエンドプロセス
  - パーティションテーブル
    - アプリケーションからは完全に隠蔽される

### architecture

- WAL: Write Ahead Logging
  - Consistency を保つための仕組み
  - WAL バッファ
    - メモリ・ディスクにログデータ化
    - チェックポイントによるテーブルデータ化
- VACUUM
  - テーブルのデータを整理・再配置
- **SLRU**
  - Simple Latest Recently Used
  - **トランザクションのコミット状態**などは、頻繁にアクセスされるため、メモリ上にキャッシュされている
- 増分バックアップ
- **メンテナンス専用権限の追加**
  - MAINTAIN 権限
- **EXPLAIN 文の拡張**
  - 実行計画作成時のメモリ設定を出力する MEMORY オプションが追加された
  - `EXPLAIN (MEMORY) SELECT * FROM users;`

### SQL

- COPY 文
- JSON 関連の追加
  - JSON コンストラクタ
  - JSONPATH メソッド
  - JSON 変換
  - JSON 検索
- https://www.postgresql.org/docs/17/functions-json.html#FUNCTIONS-JSON-CREATION-TABLE

``` sql
-- JSON コンストラクタ.
test-db=# SELECT JSON('{ "val": 1 }'::bytea FORMAT JSON ENCODING UTF8);
     json     
--------------
 { "val": 1 }
(1 row)

test-db=# SELECT JSON_SCALAR(123.44::numeric);
 json_scalar 
-------------
 123.44
(1 row)


test-db=# SELECT * FROM json_table('[
{"key1": "value1", "key2": 2},
{"key1": "value3", "key2": 4}
]'::jsonb, '$[*]'
  COLUMNS (
    id FOR ORDINALITY
    , colkey1 text path '$.key1'
    , colkey2 int4 path '$.key2'
  )
);
 id | colkey1 | colkey2 
----+---------+---------
  1 | value1  |       2
  2 | value3  |       4
(2 rows)
```

### merge

- BY SOURCE 句の追加
- RETURNING 句のサポート
- Links
  - https://ja.wikipedia.org/wiki/MERGE_(SQL)
  - https://www.postgresql.jp/docs/15/sql-merge.html

### memo

``` sql
\l

test-db=# \conninfo
You are connected to database "test-db" as user "postgres" via socket in "/var/run/postgresql" at port "5432".

-- メタコマンドのヘルプ表示。
test-db=# \?


-- 3s おきに実行、結果が 1 行以上ある場合は繰り返し表示。
test-db=# \watch i=3 m=1
Sun 26 Jan 2025 12:36:40 PM UTC (every 3s)

 id | colkey1 | colkey2 
----+---------+---------
  1 | value1  |       2
  2 | value3  |       4
(2 rows)


WITH time_ranges AS(
  SELECT unnest(ARRAY[
    tsrange()
  ])
)
```

