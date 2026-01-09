## ORM

- Prisma
  - 抽象化されすぎてて発光されるクエリが微妙になることも
  - migration/sql で高度な表現が使えない
      - RLS, TRIGGER など
- Drizzle
  - SQL ライクな書き方と抽象化された API の 2 通りある
  - 生成が不要なので CICD の構成が楽
- **Drizzle と一緒に使うといいライブラリ**
  - **AsyncLocalStorage**
    - **バケツリレー的な実装からの脱却**
    - リクエストに紐づく db connection にアクセスできるなど
    - **トランザクション管理も直感的に行える！！**
  - **praha/drizzle-factory**
    - テストデータの生成を支援
    - Factory Bot (Rails) のような発想

## なんでも
