## 0

ソーシャルログイン

- SNS に代表される ID プロバイダがユーザー認証を肩代わりしてくれる
- IdP から受け取ったユーザーの属性を利用して登録を簡略化
- IDaaS に任せるのがおすすめ
  - Firebase Authentication とか

## sec 1

### ユーザー認証

- パスワード認証
  - 課題
    - パスワードの失念
      - アカウントリカバリー処理
    - 使い回し
    - 推測されやすい値
    - フィッシングアプリへのパスワード入力
      - フィッシング攻撃は、二要素認証では防げない。、、

パスワードリスト攻撃やパスワードスプレー攻撃の対策として、二要素認証が有効。

### FIDO 認証

- パスワード認証がかかえる様々な課題を解決する
  - 脱パスワード認証として提唱されている
- **ユーザーとサーバーで秘密の情報を共有しない！**
  - 手元の端末が提供する認証機能によってユーザーの認証が行われる
- ブラウザ: WebAuthn という API
- ネットワークでやり取りされるのは乱数とその署名
- 課題
  - リカバリー方法
  - 理想は認証器2つ
  - 現実的にはパスワード認証などの代替の準備が必要
    - 結局ココが狙われる

### ソーシャルログイン

- ID 連携も！
- リライングパーティー
  - ID 連携を受け取るアプリのこと
- 注意点
  - IdP ごとに仕組みが微妙に異なる
  - リカバリーの処理が必要
    - SNS ユーザーが利用停止された場合など
  - ID 管理の各種機能の実装が必要になる
    - IDaaS のすすめ

### ID

- Identity
  - IdP
  - ID 連携
- Identifier
  - user id
  - client id

### IDaaS

- Identity as a Service
  - アイダース、アイディーアース
- 主な機能
  - ユーザーのログイン
  - ユーザーの ID 管理機能
  - 外部サービスとの ID 連携機能
  - ユーザーの権限や状態に応じたアクセス制御
- 企業システム向け IDaaS
- コンシューマアプリ向け IDaaS
  - ターゲット
  - Firebase Authentication, Auth0, AWS Cognito, Azure Active Directory
- IdP と直接やりとりするのは IDaaS になる


## sec 2

### Firebase CLI

``` sh
npm instal -g firebase-tools

firebase --version
11.29.1

firebase login
```

### Firebase Hosting

https://firebase.google.com/docs/hosting?hl=ja

``` sh
firebase init
# Hosting: Configure files ...
# Use an existing project

firebase deploy
```

