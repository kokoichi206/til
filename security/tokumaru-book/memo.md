## sec 3

### 3.1

https://chat.openai.com/share/fec9836a-86d7-49dd-97bf-edb9cfacd047

- basic 認証のキャッシュ削除
  - `https://username:password@www.example.com/`
  - https://dev.classmethod.jp/articles/delete-cache-for-basic-authentication/
  - Firefox を Quit した後に立ち上げ直すと、再度ログインを求められた
    - Firefox アプリのメモリ上に持たせてる説ある

疑問

- hidden パラメーターを使うメリットのところ
  - https://groups.google.com/g/wasbook-readers/c/8_G_J1aHGfc
  - https://blog.tokumaru.org/2013/09/cookie-manipulation-is-possible-even-on-ssl.html
- セッション ID の固定化攻撃
  - クッキーモンスターバグ
    - どうやって `kanagawa.jp` に cookie を発行できるアプリかを見分けてる？

### 3.2

- サイトをまたがった受動的攻撃
  - リクエストで攻撃
    - CSRF
  - レスポンスで攻撃
    - XSS
    - HTTP ヘッダ・インジェクション
- ブラウザはどのように受動的攻撃を防ぐか
  - サンドボックスという考え方
  - 同一オリジンポリシー
    - ブラウザのサンドボックスに用意された制限の1つ
  - 一度に複数のサイトのオブジェクトを扱うことができる
    - タブ
    - frame
- 同一オリジンポリシー
  - ブラウザが拒否してくれている？
    - プリフライトリクエスト
  - 同一オリジンである条件
    - ホスト
    - スキーム
    - ポート番号
  - iframe のなかに js を送り込んで実行する手法が XSS
  - JSONP
    - JSON with padding
    - 他オリジンに対する script タグ
  - form 要素の action 属性
    - CSRF
    - 意図しない form 

### 3.3

- 『シンプルなリクエスト』の場合、異なるオリジンに HTTP リクエストを**送ることが相手の許可なしに可能**
  - これはシンプルなリクエストの例だわ
  - [readyState](https://developer.mozilla.org/ja/docs/Web/API/XMLHttpRequest/readyState)
  - header
    - `application/x-www-form-urlencoded`
    - `multipart/form-data`
    - `text/plain`
  - js として使うには `Access-Control-Allow-Origin: http://example.jp` がサーバーからのレスポンスのヘッダーに必要
    - 応答ボディはスクリプトには利用できません (理由: CORS Missing Allow Origin)
    - **情報が返るのは問題なくて、中身の js に使われるのが問題**
      - スクリプトとして使われなければ大丈夫そう
- プリフライトリクエスト
  - **『シンプルなリクエスト』を満たさない場合、ブラウザが pre-flight request という HTTP リクエスト**
    - OPTIONS リクエスト
  - 応答ボディはスクリプトには利用できません (理由: CORS Missing Allow Header)
  - やり取りするヘッダ
    - OPTIONS を突破した後は、シンプルなリクエストと同等の扱い
  - プリフライトリクエストでやり取りするヘッダ
    - メソッドに対する許可
    - ヘッダに対する許可
    - オリジンに対する許可
- 認証情報を含むタイプ
  - `Access-Control-Allow-Credentials: true`
  - クライアントが自分が持ってる認証情報をつけたいかどうか
    - `withCredentials = true`
  - js で操作を許可する
    - `Access-Control-Allow-Credentials: true`


## Links

- [XMLHttpRequest](https://developer.mozilla.org/ja/docs/Web/API/XMLHttpRequest)
