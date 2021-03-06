## なんでも

- WebAuthn: Web Authentication
  - Web サービスなどにログインする際に、パスワードの代わりにスマートフォンなどのデバイスが持つ認証機能を使用できるようにする技術仕様
  - FIDO2
- 盗み聞き
  - ポテチの菓子袋、ティッシュ箱、コップの水面、などを高速度カメラで撮影し、「部屋内の音声」を復元する技術
  - 音声の「空気の揺れ」は毎秒２万回
    - 人が聞き取れるのは 100-20000 Hz
- 粒度: granularity <- grain
  - 関数の粒度
  - コミットの粒度
    - このコミットは ○○ です
  - レポートの粒度
    - エグゼクティブ・サマリー
  - コミュニケーションの粒度
- SoC: System On Chip
  - NVIDIA の手掛ける、GPU, CPU, AI 機能などをバランスよく搭載したもの
  - 車載、ゲーム、Switch, Audi など
  - NVIDIA Orin
- HeatWave ML
  - MySQL のマネージドデータベースサービスである、MySQL HeatWave Database Service で利用できる機械学習プラットフォーム
- リバースブルートフォースアタック
  - パスワードを固定して ID を変えながら認証されるかを確認する攻撃手法
  - パスワードを一定回数間違えるとアカウントロックがかかるシステムが増えてから流行ってる手法
- セキュリティ
  - OpenCTI
  - セキュリティは総合格闘技
- Terraform
  - メリット
    - コードの順番に関係なく全体を把握して適切な順序で実行してくれる
  - デメリット
    - ミドルウェアやサーバソフトウェアのインストールには別途シェルスクリプトなどを利用する必要有
    - いろいろなことを「環境変数」に定義する必要がある
- Ansible と Terraform は合わせ技で使うのが良い！
  - Ansible:
    - サーバやミドルウェアの設定情報構成管理ツール
  - Terraform:
    - インフラの構成情報管理ツール

## API

### Web API とは

- API の種類
  - ハードウェア API / OS API
  - インターナル API
  - パブリック API (利用)
  - パブリック API (提供)
- Web API
  - HTTP というネットワーク間通信のためのプロトコルを使用
  - リモートでソフトウェア/サービスを操作するためのインタフェース
- 背景
  - UX を提供するインターフェース・ソフトウェアの増加
  - サービスの持つビジネスロジックを抽象化し、UI/UX からの再利用生を向上させたい！
- マッシュアップ
  - 外部のサービスを組み合わせて新しいサービスを提供すること
- 技術要素
  - HTTP: ベースプロトコル
  - Web API としてのスタンダードな仕様の検討
    - REST, OData, SOAP, GraphQL, gRPC
  - REST
    - Addressability
    - Uniform Interface
    - Client-Server/Stateless
    - Connectability
      - nextPage: ...
  - REST はプロトコルや規約ではなく、あくまでも Web API の設計思想！
    - アーキテクチャスタイルの１つ
  - その他要素
    - OAuth, Basic などの認証・認可
    - Web API のテスト
    - キャッシュ
    - クッキー
- DX: Developer Experience

### REST API

- 6 原則
  - クライアント/サーバ
  - ステートレス
    - サーバー側に状態を保存せず（セッションを利用せず）リクエストの中に必要な情報を全て含める
  - キャッシュ制御
  - 統一インターフェース
    - リソースの識別
    - 表現を用いたリソース操作
    - 自己記述メッセージ
    - HATEOAS
      - レスポンスに現在の状態をふまえて関連するハイパーリングを含める
      - ブログ記事のレスポンスで、次の記事へのリンクなど
  - 階層化システム
    - Web, App, DB とか
  - コードオンデマンド
- REST 設計レベル
- URI がリソースの集合、を表現しているため、複数形が適切
- クエリとパス
  - データを一位に特定するための情報（≒ 必要な情報）かどうかで使い分ける
  - ユーザー ID のようにユーザーを一位に特定して情報取得させたい場合、パスを使った URI 設計
  - 検索条件のように、複数の非必須の複数条件を指定させたい場合は、クエリを使用する
- 503 + Retry-After
- API の認証
- レートリミット
  - 誰に対して、何に対して、制限回数、単位時間
- リクエスト観点
  - サーバ側のアーキテクチャを反映しない！
  - 不明な省略を行わない！
- レスポンス観点
  - ステータスコードの利用
  - エンベロープを使用しない
- 「利用者観点」の設計が何より大事

### OpenAPI を用いた Web API 開発

- スキーマファーストな開発が可能
- OAS という標準化された仕様
- OpenAPI generator など
- swagger-cli
- Prism を利用したモックサーバの活用

## DNS

Route 53, Cloud DNS

### DNS とは

- 30 年以上の歴史があり、それがずっと動き続けている！
- インターネットは DNS に大きく依存している
- DNS 以前
  - HOSTS.TXT を全世界で共有！？
- クライアントプログラムは、名前解決をフルサービスリゾルバに依頼
  - リゾルバはたとえば ISP や会社のネットワークに設置された DNS キャッシュサーバ
- DNS は ROOT サーバから多段の権威サーバによる、階層で管理された巨大な分散データベース！！
  - ROOT サーバは 13 個しかない！
- DNS でやりとりされるデータは UDP で 512 バイトが基本
- 独自の DNS サーバプログラムに変えることで、Twitter の名前解決を行わない、などもできる

### DNS の名前解決

- ドメイン名空間
- 完全修飾ドメイン名
  - ルートラベルのドットも含めたもの (`www.example.com.`)
- 相対ドメイン名
  - 最後の方から１つ以上のラベルを省略したもの (`example.com`)
- ドメイン上から
  - ルートドメイン、トップレベルドメイン（TLD）、セカンドレベルドメイン（SLD）
- サブドメイン
  - "com", "jp" 等はルートドメインのサブドメイン
  - "example.com" は "com" のサブドメイン
- ゾーンと権威
  - "example.com" は "example.com" をゾーン頂点（zone apex）とする
  - ゾーンに対して権威を持っているサーバを権威サーバと呼ぶ
- リソースレコード
  - A:
    - IPv4 の IP アドレス
  - AAAA: クアッド・エイ
    - IPv6 の IP アドレス
  - CNAME:
    - 正式名を意味し、別名を定義するときに使う

```sh
dig com NS
ping -c1 www
```

### セキュリティ

- キャッシュポイズニング攻撃
- ソースポートランダマイゼーション
- UDP ではなく TCP を使う、とかも
- MyEtherWallet 事件
