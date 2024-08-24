## なんでも

- [WinterJS](https://github.com/wasmerio/winterjs)
  - **Wasmer (Wasm ランタイム) の開発元が発表した OSS の JS ランタイム**
  - サーバーサイドでの使用を想定している
  - 特徴
    - 爆速
      - Bun, Nodejs よりも高速
    - Wasm バイナリにコンパイルして Web Assembly ランタイム上で実行可能
      - **この場合 JIT コンパイラによる実行時最適化ができないためパフォーマンスは落ちる**
    - Rust 製
    - **互換性**
      - とくに, Cloudflare Workers とは高レベルの互換性を持つ
      - WASIX
- ドメイン
  - 攻撃の手法
    - **名前解決の偽装**
      - DNS キャッシュポイズニング
    - **DNS の権威サーバのリソースを食い尽くす**
      - DDoS 攻撃
      - DNS 水責め
  - DNSSEC
    - キャッシュサーバから権威サーバに問い合わせて帰ってきた応答が、
    - ドメイン所有者の意図したものでありかつ改竄されてないことを担保してくれる
- DI: Dependency Injection
  - コンポーネント間の依存関係を管理するための手法
  - コンポーネントを抽象化することで
    - 実装の詳細から切り離すことができる
    - コードの変更が他の部分に与える影響を最小化
  - うーん、インターフェースの説明と同義じゃない？と思ったけど、インターフェースに依存した設計にしたら DI せざるを得なくなるから一緒でいいのか
  - IoC: Inversion of Control
    - 制御の流れを反転させる原則
    - 外部のコードが制御の主体となり、アプリケーションコードを呼び出す！
  - DIP:
    - **ソフトウェアを柔軟に保ち、ビジネスロジックを技術的な要素から守る**
    - **入出力からの距離を示すレベル**
      - 低レベルは機械に近い具体
      - 高レベルは人間に近い抽象
- RDBMS
  - 統計情報から使用を確認
    - `pg_stat_user_table`

``` sql
SELECT
    relname AS table_name,
    seq_scan,
    idx_scan,
    n_tup_ins,
    n_tup_upd,
    n_tup_del
FROM pg_stat_user_tables;
```

- chrome
  - PWA: Progressive Web App
    - Service Worker
    - Web App Manifest
    - ネイティブの持つ　API
  - Progressive Enhancement
    - コアな Web ページをまず表示できるようにし、負荷的なレイヤを段階的に追加する戦略！
    - 後方互換の考え
      - **エスカレーターとエレベーター**
      - **エスカレーターみたいに作るべき！**
  - Web App Manifest
    - インストールされたときに、どのように動作するかを記載する JSON ファイル
  - Service Worker
    - **メインスレッドのバックグラウンドで動作する JavaScript 実行環境**
    - ブラウザとサーバーの通信の間でプロキシのような役割を担う
    - プッシュ通知など
  - **Project Fugu**
    - ネイティブアプリができることを Web でもできるように Chrome チームが進めているプロジェクト
    - [features](https://developer.chrome.com/docs/capabilities/status?hl=ja)
      - Push API
      - Badging API
      - WebUSB API
      - etc...
- **アーキテクチャ特性**
  - 特性
    - 可用性
    - 信頼性
    - テスト容易性
    - スケーラビリティ
    - etc...
  - アーキテクチャ特性同士の競合やトレードオフ
- AWS
  - [Amazon Q](https://aws.amazon.com/jp/blogs/news/introducing-amazon-codewhisperer-for-command-line/)
  - `cw ai`

## SQL

- リレーション
  - **集合(数学)**
    - 要素のコレクション
    - 重複なし
    - 要素間に順序なし
- リレーション構成要素
  - みだし
  - 本体
    - タプルの集合
    - 属性値
    - 属性
      - 名前とデータの型
- 演算
  - SQL and Relational Theory
    - 洋書かつ鈍器のような本w
- テーブル
  - SQL においてリレーショナルの概念を体現してるのはテーブル
  - タプルは行、属性は列
  - **SQL 演算の入力はテーブル、結果もまたテーブル**
  - **テーブルはリレーションではない**
    - 列に順序がある
    - 行が重複できる
    - NULL を許容している
  - **テーブルを限りなくリレーションに寄せて使うことで、リレーショナルモデルの利点を最大限引き出せる**
- リレーショナルモデルをベースにする利点
  - **検索条件を記述するだけで RDBMS 側にその取得方法を任せられる**
    - クエリを実行する方法を決めなくていい
  - **→ 宣言的にクエリを記述することが可能**
  - SQL を記述するときは**可能な限りリレーショナルモデルを活用する！！**
- リレーショナルモデルとインデックス
  - index はデータアクセスの実装の話
  - **SQL 標準でも標準化されておらず, INDEX という単語も SQL の予約後ではない！**
  - 正規化理論
    - 候補キーはあるが、主キーはない

### 実行計画

- データベースサーバ
  - Parser
  - Optimizer
  - Executor
- オプティマイザ
  - コストの見積もり
    - JOIN の順番を入れ替える
    - インデックスを利用するか否か
  - コストベースオプティマイザ

``` sql
desc employees

-- FORMAT=JSON などもある。
EXPLAIN FORMAT=TREE SELECT * FROM employees WHERE xxxx;
```

### インデックスの機能

- MySQL では**インデックスの実装はストレージエンジンによっている**
  - InnoDB
    - B+ tree
    - 空間インデックス
    - フルテキストインデックス
- B+ tree インデックス
  - tree
    - グラフの一種
    - グラフ
      - 複数のノード間がエッジによって接続
      - 階層が定義された有向グラフ
  - 階層
    - レベルとも呼ばれている
  - **現実のテーブルではデータが隙間なく埋まってることはほとんどない**
    - 挿入・削除を繰り返すうちに、恒常的に空き領域が生じる

## [Bun](https://github.com/oven-sh/bun)

- Zig 製
- 背景
  - Node.js の複雑化
    - パッケージ管理の複雑さ
    - モジュールシステムの問題
  - Deno の登場
    - Deno の特徴
      - package.json, node_modules, CommonJS のはいし
      - ビルドインのテストランナー
      - TypeScript の標準サポート
    - Node.js との互換性が渋かった
- Bun の特徴
  - **オールインワンな JavaScript ランタイム！**
  - とにかく速い！
  - Node.js, Jest との互換性
- 機能
  - CLI
  - パッケージマネージャー
  - Bun Shell
    - **JS や TS でシェルスクリプトを書くことができる機能！**
    - 特徴
      - クロスプラットフォーム
      - bash ライクなシェル
      - js, ts との相互作用
