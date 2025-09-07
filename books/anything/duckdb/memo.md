## introduction to duckdb

- モダンな組み込み型の分析データベース
- 複数のソースから GB 単位のデータに対して効率的にクエリを実行できる
- DuckDB のクエリ処理
  - SQL パーサー、クエリ実行プランナー、クエリランタイム
  - クエリエンジンはベクトル化されている
    - => マルチコア CPU の性能を最大限に活用
- データパイプラインとデータの準備が簡素化される
- いつ使うか
  - 前提
    - データが利用可能な状況（not streaming）
    - データが数百 GB を超えない
- Summarize 句
  - https://duckdb.org/docs/stable/guides/meta/summarize.html
- DuckDB
  - 分析データベース、インメモリ処理に優れている
