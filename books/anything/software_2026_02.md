## Vibe Coding

### Getting Started

- Vibe Coding
  - 狭義
    - AI の提案に全面的に委ね、コードをいっさい確認しない
  - 広義
    - 自然言語で指示を元に AI がコードを生成
    - 必要に応じて人間がコードの確認・修正に介入する
- Agentic Coding
  - Vibe Coding とは異なる考え方であるが、ここでは広義の Vibe Coding に含める
- gpt-5-coding-examples
  - https://github.com/openai/gpt-5-coding-examples
- エンジニア
  - マネジメントする人
    - 何をなぜ作るかの言語化
  - 個人の可能性
  - 誰もが開発者

### コンテキスト設計

- 計画、実装、検証、のフェーズ
- 計画
  - 最新かつ信頼できる情報源、を AI エージェントに与える仕組み
  - **計画フェーズで要件定義・詳細設計を完璧に決めすぎないこと**
    - 完璧にやろうとすると AI コーディングの良さが消える
    - スピードが犠牲になる
  - **大事なこと**
    - 計画の範囲を事前に決めておく
    - 手戻りを恐れない
- 実装
  - **客観的な観測情報**を AI に渡せるようにする
- 検証
  - 小さく実装・すぐに検証
- SKILLS
  - Progressive Disclosure
    - just in time
- Context
  - Context Rot
    - 回答に有効な情報を抽出・活用できなくなる現象

### ガードレール

- ガードレール
  - 前処理
  - 処理中
  - 後処理
- **知識を LLM に渡す手段**
  - RAG: Retrieval-Augmented Generation
  - Web 検索
    - 遅い、結果が博打要素ある
  - llms.txt
    - **HTML は UI の情報を含むため、正確な情報を得る手段としては最適ではない**
    - => AI フレンドリーなデータ
    - 信頼性が高い
  - ツール呼び出しと MCP
    - コンテキストウィンドウで保持するしか方法がないためベストであるケースが少ない
    - => **静的な情報を受け取る手段どしてはベスト効率ではない**
  - **CLI/ローカルドキュメント**
    - Bun
      - bun-types
    - Hono
      - Hono CLI => CLI 経由でのドキュメント
- **仕様に沿っているか**のガードレール
  - TODO リスト
  - Figma MCP
- コードが正しいか
  - Linter/Formatter
  - ユニットテスト/e2e テスト
  - 視覚的な検証手段
  - コードレビュー
- 具体例
  - ドキュメントをローカルに落とす
  - OSS を GitHub からクローンしておいておく
  - Linter/Formatter は高速なものがいい

### 攻略する

- 課題
  - AI モデルの問題
  - AI エージェントの問題
- 仕様駆動開発
  - 中〜大規模の開発で Vibe Coding で意図した実装を実現
- メンテナンス
  - 誰が保守すべきか？
    - 人間派
    - AI 派
  - **保守しやすいコードを生成させる**
    - ドキュメント生成
      - 自動生成
      - 人間が補完ドキュメント
        - 実装計画書
        - 実装記録
        - 仕様書
    - 定期的な設計の見直し
- コードに対する理解
  - DeepWiki の活用
- **レビューがボトルネックになる**
  - コードレビューを AI にさせる
- OWASP top 10
  - https://owasp.org/Top10/2025/
- ツールが進化すればするほど、それを使いこなすには人間の基礎力が重要になる

## S3

### S3

- イベント駆動の起点にも
- **オブジェクトストレージ**
  - 以下の3つからなる
    - データ本体
    - メタデータ
    - 一意に識別するキー
  - バケット
    - アクセス制御等
  - キー
    - **フォルダという概念は存在しない**
    - キーの命名 = 設計
- クラス
  - 標準
    - 3AZ 以上で冗長化
    - イレブンナインの耐久性
  - S3 One Zone-IA
    - 半額くらい
- 経路
  - Private Instance => Gateway VPC Endpoints => S3

### こんなことあんなこと

- データの変化をイベントとする
  - Lambda/EventBridge 等
  - EventBridge を挟んだほうが、条件に応じた分岐・複数サービスへの連携が容易
    - 疎結合であり推奨される
- 静的ファイルの配信
  - CloudFront => S3
- データ保護
  - バージョニング
  - レプリケーション
  - **オブジェクトロック**
    - WORM: Write Once Read Many
- コスト感
  - **小さなファイルはまとめて圧縮する**
    - Athena とかでクエリかける時はどうなる？

### データ基盤の中心として

- データの分類
  - 構造化データ
    - 固定帳ファイル
    - CSV
    - RDB 内データ
  - 半構造化データ
    - XML, JSON, YAML
    - HTML
    - Avro
  - 非構造化データ
    - メール、テキスト
    - 画像、動画、音声
- データの考え方
  - **意味レイヤ（Semantic Layer）**
    - S3 Vectors
    - 非構造化データの意味づけ
    - Bedrock, Nova
  - **構造レイヤ（Table Layer）**
    - S3 Tables, Apache Iceberg
    - Athena, Redshift が効率よく読み取れるようにする
  - **メタデータレイヤ（Metadata Layer）**
    - カタログのように整理して扱える
    - Glue Data Catalog
- Operations
  - S3 Batch Operations
  - メタデータ管理の整備
    - => どこに何のデータがあるか、を明確に把握できる、**データカタログ**へと
- データ基盤全体の流れ
  - **データがどこからきて、どのように蓄積されて、どのように活用されるか**
  - データソース => データレイク => Lakehouse, DWH => BI/AI
- **データレイク**
  - **三層モデル**
    - Raw
    - Processed
      - 整形データ
    - Curated
      - 分析用

## なんでも

- WebXR
  - Three.js
    - React-Three-Fiber
- DDoS-DNS
  - L3/L4 
    - ここへの DDoS はインフラへの攻撃で、**ボリューム型攻撃**とも呼ばれる
    - 手法
      - **帯域を埋める攻撃**
        - UDP フラッドなど
      - **接続管理機能を麻痺させる**
        - OS/ファイヤフォール管理のセッションテーブルなど
        - SYN フラッドなど
          - DNS でも DNSSEC などの普及で TCP に対する攻撃を想定する必要がある
  - L7
    - サーバーダウン
  - DNS 特有
    - DNS 水責め（**ランダムサブドメイン**）
      - 権威サーバーへ過剰アクセスを飛ばす
- test 自動化
  - **継続して使い続けられること**が大事
    - そのために必要な性質
      - 信頼性
      - 高速性
      - 保守性
      - 明視性
        - 誰もがテスト結果を閲覧でき理解できる
      - 保全性
- TLS
  - ASN.1, DER
  - ASN.1: Abstract Syntax Notation One
    - **データ構造を特定の言語やハードウェアに依存せずに記述するための記法**
    - schema のようなもの
    - **以下を明確に分離**
      - 抽象構文: データの意味
        - Abstract Syntax
      - 転送構文: データのバイト列表現
        - Transfer Syntax
  - Transfer Syntax
    - **エンコーディングルール**
    - BER: Basic Encoding Rules
    - DER: Distinguished Encoding Rules
      - TLS で使われる
      - 一意に定まるようにした BER のサブセット
      - **同じデータ構造は常に同じバイト列になる**
      - 署名検証などで必要
- IPv6
  - 1995 年に標準化されてすでに 30 年経過してる！
  - IPv6 は人間が覚えることを想定していない
    - **IPv4 との違い**
      - 人間中心の運用 vs 機械中心の運用
  - IPv6 にするメリットが今までなかった
    - AWS が IPv4 アドレスに課金してきてることで状況が変わりつつある
    - IPv4 の枯渇が深刻に

## podman

``` sh
podman run --rm quary.io/podman/hello
```

- Docker との compatability がいまいちわかってない
  - https://podman-desktop.io/docs/migrating-from-docker/managing-docker-compatibility
