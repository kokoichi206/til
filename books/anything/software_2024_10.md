## なんでも

- Skip
  - **Swift で iOS/Android アプリが作れる**
  - Swift コードを Kotlin コードに変換するトランスパイラが機能している
    - Apple の提供する SwiftSyntax ライブラリを使用して Swift コードを解析している！
  - **SwiftPM での内容を Android Gradle のプロジェクトに変換することもしている！**
    - Skip Stone
  - 特徴
    - 追加のランタイムが不要でメモリ効率がいい！
    - 元になる Swift と生成された Kotlin コードは、いずれも Skip なしで単独でも使用可
- MX レコード
  - 電子メールの仕様上、送り主として表示されるヘッダの From には任意のメールアドレスを記載できる
  - MX レコード
    - A レコードと違い、**優先度を設定できる！**
  - SPF
    - 送信元アドレスの詐称を防ぐため
  - DKIM
    - **送信サーバの秘密鍵で**メールヘッダと本文に**電子署名**
      - **受信側が、DNS から入手した公開鍵で検証**
    - 公開鍵は DNS で TXT レコードとして登録
  - DMARC
    - 認証結果を元に、レポーティングやポリシー適応を行う
  - **増え続ける DNS の役割と負荷**
    - DNS はそのドメインの所有者だけが情報を編集できる場所
      - **→ ドメイン所有権をトラストアンカー（信頼の起点）とするサービスに幅広く利用される**
- ソフトウェアテスト
  - 不定動作
  - テストケース
    - 仕様をサンプリングして得た入力とその期待出力の組のこと
- レガシーシステム改善
  - BFF の導入背景
    - 通信量の増大
    - パーソナライズ機能の追加
      - ユーザー情報に応じた
  - キャッシュの導入
    - Redis
  - **キャッシュの有効期限が一斉に切れることによるリクエストのスパイク**
    - Cache Stampede
    - Dog piling
  - **Istio によるサーキットブレーカー**
    - サービスの障害を検知した場合には通信を遮断、その後サービスの復旧を検知すると通信を復旧
- Databricks
  - **データレイクハウス**
    - **データウェアハウスとデータレイクの長所を組み合わせた**
  - Databricks
    - オープンデータレイク
    - Delta Lake
      - 信頼性と共有のための統合データストレージ
    - DatabricksIQ
    - Databricks SQL
      - Databricks におけるデータウェアハウスの機能
- Chrome の世界
  - Cookie
    - **ファーストパーティ Cookie**
      - 訪れているサイトと同じサイトに送る Cookie
    - **サードパーティ Cookie**
      - 訪れているサイトではないサイトに対する Cookie のこと
      - **異なるサイト間でユーザーを識別する目的**
  - サードパーティ Cookie のユースケース
    - ログイン
    - 計測
    - トラッキング
  - サードパーティ Cookie の問題
    - 意図しないサイトに情報が付与される
    - ユーザーの同意なしに使われてきた
  - プライバシーに関する議論の加速
    - EU 一般データ保護規則, GDPR がでかい
  - サードパーティ Cookie をブロックすることの問題
    - この辺を区別したいが、Cookie だけを見て判断は不可
      - ログインは有用な使い方
      - **問題なのはトラッキングのみ**
    - 広告と Web のエコシステムへの影響
    - **別のトラッキング方法が使われることへの懸念**
      - Cookie 以外のトラッキング
        - フィンガープリンティング
  - **Privacy Sandbox**
    - 幾つかの取り組みと API 群からなるプロジェクト
    - ユースケースごとに API を作ることで、**クライアント側で用途を知る手段がないという点を解決！**
    - サードパーティ Cookie のような振る舞いを実現できる、用途や影響を絞った API を複数用意
  - Privacy Sandbox の API 5種類
    - スパムを防ぐ
      - Private State Token API
    - 関連広告を表示する
    - デジタル広告の計測
    - 異なるサイトでのプライバシー協会を維持しつつ利便性も維持
    - 隠れたトラッキングを防ぐ
      - フィンガープリンティングを防ぐための取り組み
- 開発者体験
  - 早く失敗すればいい
  - **ゴールがどこにあるかを大切にする**
  - Design Maturity Levels
    - https://www.figma.com/community/file/1177474796269267037/design-maturity-levels
- Cloudflare Workers
  - Durable Objects
    - トランザクションストレージ
    - 強整合性をとれる KV store
    - Cloudflare Workers KV は結果整合性
      - **エッジ間同期前に同じキーに対して書き込みがあった場合、書き込みタイミングが遅い方で上書きされる**
    - WebSocket によるリアルタイム通信が可能！
      - これまで, Cloudflare Workers のようなライフタイムの短いサーバーれる環境では実現できなかった
- インターネット
  - ネットワークの正体
    - **ルータの集まり**
    - ISP の場合、一般には数十〜数百のルータでネットワークが構成されている
  - AS ネットワーク
    - 1つの組織が保有・運用しているネットワーク全体
    - Autonomous System: 自律システム
    - AS 番号
      - BGP などのルーティングプロトコルにおける設定情報として利用される

## 設計ドキュメント

- ドキュメントへの投資
  - 請負・準委任
    - 請負
      - 成果物の完成を作るもの
    - 準委任
      - アジャイルなど、事前に成果物定義が不可能な場合
  - 提出フォーマット
  - 開発規模
    - メンバーの入れ替わりの激しさなども関係
- 難しさ
  - ソースコードとの同期が取れず、陳腐化
    - マーフィーの法則
      - **失敗する余地があるなら、失敗する**
      - 余地をなくす
- ADR の導入理由
  - 設計ドキュメントが最新で、ソースコードと同期が取れている
  - ナレッジの一元管理
  - アーキテクチャ選択の背景をメンバー全員が認識できる
  - アーキテクチャの見直しの履歴などを残す
- [ADR-Tools](https://github.com/npryce/adr-tools)


## オンライン個人認証・本人確認

- eKYC: electronic Know Your Customer
  - how
    - 自撮り + 身分証明書
    - 身分証明書の IC チップ
- 本人確認？
  - 顧客の実在性の確認を行う身元確認のこと
  - cf: 当人確認
    - 顧客本人がサービスを利用していることを確認すること
- KYC
  - Know Your Customer
  - 顧客（取引先）確認
- eKYC
  - ホ
  - ヘ
  - ト
  - ワ
- PKI:
  - Public Key Infrastructure
  - **電子署名などを通して、情報の真正性を確保する**
    - どこで？
      - 通信で
- JPKI
  - Japanese Public Key Infrastructure
    - 公的個人認証サービス
  - 偽装への対策
    - なりすまし

