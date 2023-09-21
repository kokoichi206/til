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
