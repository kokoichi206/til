## WebXR

- WebXR
  - 画像マーカーの検知
  - 自己位置推定
- WebXR エンジンの種類
  - WebXR Device API
    - 標準 API
    - W3C の Immersive Web WG が標準化しようとしてる
  - 独自の AR エンジンを使用するライブラリ
    - WebAssenbly などにまとめて実装
- レンダリングエンジン
  - Three.js
  - Babylon.js
  - PlayCanvas
- ワールドトラッキング

## ID 管理

### デジタル ID

- デジタル ID
  - ある実体に関する属性の集合
  - **実体 = Entity**
    - 現実世界に**存在する**、個人・組織・デバイス、など
    - アプリや AI エージェントといった電子的な存在も、実体、に含まれる
  - **属性 = Attributes**
    - 特徴や性質
  - **現実世界のさまざまな実態をデジタル空間上で表現し、区別できるようにするためのデータ**
- デジタル ID の管理とは
  - ライフサイクル管理
  - アクセス管理
- **ライフサイクル管理**
  - Identity Lifecycle: ISO/IEC 24760-1
    - unknown
      - 識別できる情報が ID 管理システムに存在しない
    - established
      - 識別に必要な情報が確認され、識別子とともに登録
    - active
      - リソース利用が可能となった
    - suspended
    - archived
- **アクセス管理**
  - 誰が、何に、どの条件で、どこまで、アクセスしていいか
  - 構成要素
    - **当人認証**
    - **認可・アクセスコントロール**
- 身元確認保証レベル: IAL = Identity Assurance Level
  - KYC: Know Your Customer
    - https://www.exgen.co.jp/column/edu-016.html
- 当人認証機能
  - システムにアクセスを試みる人が ID の所有者であることを確認する機能
  - パスワード、パスキー（FIDO）、ワンタイムパスワード（OTP）送付、
  - AAL: Authentication Assurance Level
    - https://pages.nist.gov/800-63-3-Implementation-Resources/63B/AAL/
- 認証連携機能
  - **ID フェデレーション**
  - SAML, OIDC などが主要な方法
- EIAM vs CIAM
  - Enterprise ID Management vs Customer ID Management
- 証跡管理
  - EIAM では必須
- ID 管理にまつわる法律・ガイドライン
  - 個人情報保護法
    - 個人識別符号
    - 個人データ
  - NISTSP800−63
  - GDPR: General Data Protection Regulation
    - EU 域内の個人のプライバシーとデータ保護
    - **EU 域内で事業を行うすべての企業に適応される**
    - 違反時の制裁金が高額
  - デジタル社会推進標準ガイドライン DS-511

### CIAM の要素技術

Consumer Identity and Access Management

- 身元確認
  - eKYC: electronic Know Your Customer
    - 例
      - 免許証やマイナンバーカードといった本人確認書類と自分の顔
      - 公的個人認証サービス JPKI
- AAL
  - AAL1
    - 単一要素認証、またはそれ以上
  - AAL2
    - 2FA, 少なくとも1つは所有ベース
    - e.g.
      - パスワード + OTP、パスキー、PIN でアクティベートする OTP デバイス
    - フィッシング耐性
      - 利用可能でなければならない
  - AAL3
    - 多要素認証
    - ハードウェアベースの暗号化認証機が必須
    - フィッシング耐性必須
- **OTP**
  - **フィッシング攻撃に弱い**
    - **利用者自身が認証情報を手入力する**というプロセスが介在するのが痛い
  - プッシュ通知
    - OOB: アウトオブバンド認証 の一種
    - ログインを承認しますか、方式
      - => **SP800-63B で非推奨となった**
    - **認証疲れ**と呼ばれる攻撃リスク
- **パスキー**
  - WebAuthn/FIDO2
  - 高いフィッシング体制をもつ次世代の認証技術
  - **WebAuthn は FIDO2 と呼ばれる標準規格の中核をなす技術仕様**
  - 公開鍵暗号方式に基づいて生成され、オリジンと紐づけられる
  - **保管方法により２種類**
    - **同期パスキー**
      - Synced Passkeys
      - iCloud キーチェーンや Google パスワードマネージャー
      - 複数のデバイス間で同期できるパスキー
      - 利便性が高い一方で、認証の堅牢性はクラウド事業者のセキュリティに依存
        - => AAL2
    - **デバイス固定パスキー**
      - Devie-bound Passkeys
      - 特定の PC やセキュリティキーといったデバイス内の専用領域に保管
      - AAL3
- **ソーシャルログイン**
  - ID 連携の一種
- OAuth2.0
  - 認可を実現するための標準的なフレームワーク
  - 拡張性
    - **PKCE と呼ばれるモバイル向けのセキュリティ拡張のサポートとか**
- OIDC
  - **OAuth2.0 のフローに、認証結果や属性情報等の連携機能を追加した技術仕様**
  - OAuth2.0 が『データにアクセスして良いか』の認可
  - OIDC は『ログインしたユーザーが誰であるか』の認証
    - ID Token

### B2B SaaS における認証基盤構築

BillOne

- Auth0
  - 2020/5~2023/12
  - **コスト面で**
    - 他の IDaaS と比べても高い
- 5年たたずで ARR 100億
- Backend kotlin
- Cognito + 自前実装
  - API からの呼び出し

## AI のセキュリティ

- エージェント
- 攻撃手法
  - PI: プロンプトインジェクション
  - JB: ジェイルブレイク
    - 安全上の制約を解除
  - **間接プロンプトインジェクション**
    - **外部の Web サイトやメールを読み込む際に攻撃が発動する**
- **AgentFlayer**: **Black Hat USA 2025**
  - ゼロクリックで乗っ取られる可能性
  - **外部入力経由での注入**
    - メール等
  - 外部入力の過信
    - **命令とデータの混同**
  - ガードレールの不足

### 攻撃手法

- 従来のセキュリティと何が違うのか
  - 従来:
    - 決定論的な攻防
  - AI:
    - 確率的・言語的な攻防
- PI: Prompt Injection
  - **LLM が命令とデータを明確に区別できないこと**に起因
    - 動作原理そのもの
  - 直接 PI
    - Prompt Leaking
      - ノウハウの流出
      - より効果的な攻撃の足掛かり
  - **間接 PI**
    - AI が外部から取得するデータに悪意のある指示を埋め込む
    - 危険な理由
      - 検知の困難性
      - ゼロクリック攻撃の可能性
        - background でのデータの読み込みでも作動
      - 攻撃の規模拡大
      - 多様な攻撃経路
- JB: Jailbreak
  - AI モデルに設定された安全上、倫理上の制約を意図的に回避、解除する行為
  - **RLHF: Reinforcement Learning from Human Feedback**
    - **ユーザーの役に立つこと**を高く評価し学習する
    - => **従順になりがち**
    - イエスマン
  - 代表的な手法
    - 役割演技
    - 感情的
    - 創造的タスク偽装
      - 創造的な文脈だと規制を緩めがち
- **サンドイッチ攻撃**
  - **AI の認知的負荷を増大させる**

### 防ぎ方

- 多層防御
  - Input Defense Layer
  - Core Policy Layer
  - Output Monitoring Layer
- **構造かプロンプティング**
  - 外部コンテンツの分離
    - XML タグや JSON エスケープ

## オフェンシブセキュリティ

- Boot2Root
- https://info.purple-flair.nflabs.jp/

## なんでも

- サーバ署名書の有効期限
  - 短くなってきている
    - 2026/3 最長 200 days
    - 2029/3 最長 47 days
  - **サーバー証明書の危殆化リスクの低減**
  - **ACME**
    - サーバ証明書を自動的に処理するためのプロトコル
    - DNS 認証の自動化
      - => **DNS サービスの API キーを ACME クライアントが利用できる場所に保管することを前提とする**
  - 47 日になったら、証明書の更新失敗時に、失効のリスクが高まる
    - **自動化プロセスの監視**
- NIST SP800-63-3
  - https://blog.trustlogin.com/articles/2017/20171130
  - Authenticator の 9 分類
- Java25 めちゃ進化
