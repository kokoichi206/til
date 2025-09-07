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

## CLI

dot commands

```
.open
.read
.tables
.timer on/off
.mode
.excel
.exit, .quit
```

```
duckdb <option> file_name <command>
```

``` sql
DESCRIBE
SELECT *
FROM duckdb_extensions();


D INSTALL httpfs;
100% ▕████████████████████████████████████████████████████████████▏ 
D LOAD httpfs;
```

``` sql
-- 拡張子が csv の場合、自動的に CSV モードになる。
SELECT COUNT(*)
FROM 'https://github.com/bnokoro/Data-Science/raw/master/countries%20of%20the%20world.csv';
```

``` sql
SELECT *
FROM 'books/anything/duckdb/csvs/Kihonjoho_UTF-8.csv';

DESCRIBE
SELECT *
FROM 'books/anything/duckdb/csvs/Kihonjoho_UTF-8.csv';
```

``` sql
SELECT 創業年
FROM 'books/anything/duckdb/csvs/Kihonjoho_UTF-8.csv'
WHERE 創業年 IS NOT NULL;


SELECT 企業ホームページ, 法人名
FROM 'books/anything/duckdb/csvs/Kihonjoho_UTF-8.csv'
WHERE 企業ホームページ IS NOT NULL
AND 創業年 = 2025;


SELECT 創業年, MIN(設立年月日), MAX(設立年月日)
FROM 'books/anything/duckdb/csvs/Kihonjoho_UTF-8.csv'
WHERE 企業ホームページ IS NOT NULL
GROUP BY 創業年
ORDER BY 創業年;
```

- WITH 句
  - CTE: Common Table Expression
- arg_max, arg_min
  - 2番目のパラメータの最小値または最大値が最初に発生した行の列に対して、1番目のパラメータで定義された指揮を計算する

``` sql
WITH base AS (
  SELECT
    "法人番号",
    "設立年月日",
    "ステータス",
    "登記記録の閉鎖等年月日",
    CASE
      WHEN "登記記録の閉鎖等年月日" IS NOT NULL THEN 0
      WHEN "ステータス" ILIKE '%閉鎖%' THEN 0
      ELSE 1
    END AS is_active
  FROM 'books/anything/duckdb/csvs/Kihonjoho_UTF-8.csv'
  WHERE "設立年月日" IS NOT NULL
),
by_year AS (
  SELECT
    strftime("設立年月日", '%Y')::INT AS founded_year,
    COUNT(*) AS total,
    SUM(is_active) AS active_now
  FROM base
  GROUP BY 1
)
SELECT
  founded_year,
  total,
  active_now,
  ROUND(100.0 * active_now / NULLIF(total,0), 1) AS active_rate_pct
FROM by_year
WHERE founded_year BETWEEN 1960 AND 2025
ORDER BY founded_year;
```


``` sql
WITH src AS (
  SELECT
    "法人番号",
    "設立年月日",
    "従業員数",
    CASE
      WHEN "従業員数" IS NULL THEN '不明'
      WHEN "従業員数" < 10 THEN '00-09'
      WHEN "従業員数" < 50 THEN '10-49'
      WHEN "従業員数" < 100 THEN '50-99'
      WHEN "従業員数" < 300 THEN '100-299'
      WHEN "従業員数" < 1000 THEN '300-999'
      ELSE '1000+'
    END AS emp_bucket,
    strftime("設立年月日", '%Y')::INT / 10 * 10 AS founded_decade
  FROM 'books/anything/duckdb/csvs/Kihonjoho_UTF-8.csv'
  WHERE "設立年月日" IS NOT NULL
),
agg AS (
  SELECT founded_decade, emp_bucket, COUNT(*) AS cnt
  FROM src
  GROUP BY 1,2
)
SELECT founded_decade AS decade, emp_bucket, cnt
FROM agg
ORDER BY decade, emp_bucket;
```

- With 句の中で RECURSIVE も使える
  - 再起的 CTE

``` sql
CREATE TABLE src (
  id INTEGER,
  parent_id INTEGER,
  name TEXT
);

INSERT INTO src VALUES
(1, NULL, 'A'),
(2, 1, 'B'),
(3, 1, 'C'),
(4, 2, 'D'),
(5, 2, 'E'),
(6, 3, 'F'),
(7, NULL, 'G'),
(8, 7, 'H');

WITH RECURSIVE tree AS (
  SELECT id,
        id AS root_id,
        [name] AS path
  FROM src WHERE parent_id IS NULL
  UNION ALL
  SELECT src.id,
        tree.root_id,
        list_append(tree.path, src.name) AS path
  FROM src
    JOIN tree ON (src.parent_id = tree.id)
)
SELECT path FROM tree;

--
WITH RECURSIVE tree AS (
  SELECT id,
        id AS root_id,
        [name] AS path
  FROM src WHERE parent_id IS NULL
  UNION ALL
  SELECT src.id,
        tree.root_id,
        list_append(tree.path, src.name) AS path
  FROM src
    JOIN tree ON (src.parent_id = tree.id)
)
SELECT arg_max(path, length(path)) FROM tree;
```

- list_append
  - https://duckdb.org/docs/stable/sql/functions/list.html#list_appendlist-element

### SQL 拡張

- `SELECT *` の取り扱い
  - 結果のタプルが不安定になる
    - テーブル定義が変更される可能性があるため
  - DB サーバーやプロセスにメモリ負荷をかける
  - インデックスのみのスキャンを妨げてしまう可能性がある
- `EXCLUDE`
- `REPLACE`

``` sql
SELECT * EXCLUDE (資格等級)
FROM 'books/anything/duckdb/csvs/Kihonjoho_UTF-8.csv';

SELECT COLUMNS('法人.*')
FROM 'books/anything/duckdb/csvs/Kihonjoho_UTF-8.csv';
```

- insert by name
  - https://duckdb.org/docs/stable/sql/statements/insert.html#insert-into--by-name
- GROUP BY ALL
- USING SAMPLE 10% (bernoulli)
