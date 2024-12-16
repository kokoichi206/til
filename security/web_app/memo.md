セキュリティバグとセキュリティ機能

- [安全なウェブサイトの作り方](https://www.ipa.go.jp/security/vuln/websecurity.html)
- [ウェブ健康診断仕様](https://www.ipa.go.jp/files/000017319.pdf)

## 環境

- Debian 9
- nginx 1.10
- Apache 2.4
- PHP 5.3/7.0
- Tomcat 8.5
- MariaDB 10.1
- Postfix 3.1g

```sh
sudo shutdown -h now

sudo vim /private
```

OWASP: オワスプ

[OWASP ZAP](https://www.zaproxy.org/)
Foxy Proxy

## sec 2

url-encoded

- ` `: %20
- `'`: %27

GET

- 参照（リソースの取得）のみに用いる
- 副作用がないこと
  - 副作用: データの追加・更新・削除
- 秘密情報の送信は POST を使う
  - URL のパラメータでは以下の危険
    - Referer 経由で漏洩する
    - アクセスログに残る

OWASP ZAP のようなプロキシツールを用いたら、普通に hidden パラメータを改変できる。

hidden パラメータは、情報漏洩や第三者からの書き換えには強い！  
（cf. セッション・クッキー）

## sec 3

Basic 認証では、`Authorization: Basic hoge` の形のヘッダーが付与されている。（hoge = user:pw を base64）

アプリケーションの状態を覚えておくこと＝セッション管理。
クッキーは、サーバ側からブラウザに指示するもの。

- [Set-Cookie](https://developer.mozilla.org/ja/docs/Web/HTTP/Headers/Set-Cookie)

Cookie は利用者本人から参照・変更できるので、秘匿情報の格納には向いてない。  
整理番号の管理のためにのみ、Cookie を使うようにする＝ Cookie によるセッション管理。

### Cookie

セキュリティ上重要な属性は、Domain, Secure, HttpOnly。

複数のサーバーに送信されるクッキーを作りたいときは Domain を使用。（通常は**設定しなくて良い**）

Secure がついていると、HTTPS 通信にのみクッキーを送信する。

JS からアクセスできないようにするには、HttpOnly。**セッション ID には基本つける**。XSS を難しくできる。

SameSite 属性は、CSRF 脆弱性対策の1項目。  
SameSite=Lax を指定したクッキーは、他サイトから POST メソッドで遷移したときは送信されなくなる。

### JS におけるサンドボックス

- ローカルファイルへのアクセス禁止
- プリンタ等の利用禁止（画面表示まで）
- ネットワークアクセスの制限（同一オリジンポリシー）

### 同一オリジンポリシー（same origin policy）

JS などのクライアントスクリプトから、サイトをまたがったアクセスを禁止するセキュリティ上の制限。ブラウザのサンドボックスに用意された制限の一つ。
