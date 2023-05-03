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

https://github.com/firebase/firebaseui-web

IdP として利用可能なプロバイダ一覧  
https://github.com/firebase/firebaseui-web#available-providers


## sec 3

### ソーシャルログイン

リライングパーティはユーザー認証を IdP に肩代わりしてもらい、認証結果として受け取った ID トークンを検証することで、自らのアプリへログインさせる仕組み。

- 実現する仕組みは IdP によって様々
  - 標準化された仕様: OpenID Conect もある
- 登場人物
  - IdP
    - ソーシャルログインを提供する主体
    - Google, GitHub
    - 母体となる SNS があり、それらのユーザーで認証した結果をアプリに通知する
  - リライングパーティ
    - IdP と連携しソーシャルログインを備えているアプリ
    - リライングパーティは必ず事前に IdP に登録が必要
  - ユーザー
    - IdP の母体である SNS のユーザー
    - かつ
    - リライングパーティーのユーザー

### ID トークン

- IdP からアプリに対して発行されるトークン
- 署名付きの JWT: JSON Web Token
  - . 区切りで、ヘッダー、ペイロード、署名の順

### Firebase

- Firebase Auth が加わった場合
  - **Firebase Auth がリライングパーティになる！**
  - アプリは Auth API を介して属性情報を取得
- ユーザー認証を肩代わりして、ユーザーの属性情報を提供してくれるもの、と考えると、アプリからみて Firebase Auth は IdP の役割を果たしている！
  - 誰からみるか、によって IdP, リライングパーティかは変わるかも

### ID 管理機能

ID ライフサイクル管理

https://ritou.hatenablog.com/entry/2020/12/07/060000

- 未登録状態/退会状態(物理削除): unknown
- 仮登録状態: established
  - メール所持確認待ちなど
- 本登録状態: active
- 一次凍結状態: suspended
- 退会状態(論理削除): archived

**リカバリー処理**

- ログインとは別の認証 + ログインで利用する認証情報の変更
- 認証付きの登録情報変更の機能、とも言えるか
- パスワードログインの場合
  - パスワードを忘れた人にメールを送信し、そこからとんでもらう
- ソーシャルログインの場合
  - ベストプラクティスと呼べるリカバリーは確立してない
  - 今回は、メール認証 + ログインとは別の IdP との連携 でやる

ログイン = 認証 + セッションの発行

- メールリンクログイン
  - ログイン用の URL を登録済みのメールアド絵r巣に送信し、その URL を開くことでログインが完了するログイン方式


## sec 4

- バンドル
  - 複数のファイルを1つにまとめるもの
  - webpack がその役割

### 設定

SDK の設定と構成 > Config

``` sh
npm init
npm install firebase

npm install -D copy-webpack-plugin
npm install -D rimraf
```

### webpack

- モジュールバンドル
  - 複数に分かれた js のもっjーるファイルを1つにまとめること
  - 読み取り性能向上につながる
- ツリーシェイキング
  - 使われていないコードを除去すること
- webpack
  - Node.js 上で動作する、CLI のモジュラーバンドラー
  - コメント、改行を削除して小容量化（minify）
  - 

https://zenn.dev/yoshiooon/scraps/d69c67a684a559

### IdP への登録

事前に IdP にアプリを登録する必要がある！

- sec 2 での Google の時は、よしなにやってくれてた？？
  - のかな
  - Firebase は Google によって提供されているため！
- GitHub
  - Settings > Developer settings > OAuth Apps


### memo

- 登録処理時の離脱率低減がかなり大事！
- emailVerified の初期値は、信頼できる IdP か信頼できない IdP かによって異なる
- 登録ユーザー間でメールアドレスを重複させることはできない
  - デフォルト設定が
  - ソーシャルログインが使えなくなった場合の代替のログイン手段として、メールアドレスを使うってなった時に困るのでそうしてる


## sec 5

- リカバリーに必要なのは **認証**だり、ログインではない
  - ログイン = 認証 + セッションの発行

リカバリーの流れ（今回のケース）　

0. GitHub ユーザーが利用停止
1. ログイン画面 → リカバリー画面
2. 登録メールアドレスにログインリンクを送信
3. ログインリンクから、ログイン完了
4. 別の IdP （Google とか）と連携

### メールリンク

Firebase でメールリンクログイン（pw なしでログイン）

https://firebase.google.com/docs/auth/web/email-link-auth?hl=ja&authuser=0

メールリンクログインを有効にする、

### リスクベース認証

- パスワードに加えてメールや SMS の確認をやったことがあるなら、リスクベース認証と呼ばれる仕組みが働いているかも！？
- IP アドレス、時間帯、位置、デバイスなどの情報を蓄積した上で、これらの情報が普段のパターンと異なるなど、不正なアクセスの可能性がある場合にのみ追加で認証を求める方式

### memo

- リカバリー画面で入力された画面で打ち込まれたアドレスが存在してもしなくても、メッセージは同じにしてる
  - 第三者による判別を防ぐため
- CSRF: クロスサイトリクエストフォージェリー
  - メールアドレスとログインリンクとの対応を確認する


