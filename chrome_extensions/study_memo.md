## 詰まったところ
- 写真が反映されない
  - [このURL](https://teratail.com/questions/109147)

  - iframe問題
    - エラーメッセージ
    ```
    The page delivered both an 'X-Frame-Options' header and a 'Content-Security-Policy' header with a 'frame-ancestors' directive. Although the 'X-Frame-Options' header alone would have blocked embedding, it has been ignored.
    ```
    - よくわからん、imageにurlつけたら解決？？はしてないかもやけど表示はできた


## メモ
- [jsのコーディング規則 @google](https://google.github.io/styleguide/jsguide.html)

- Content Script
  - 指定したページで実行されるjavascript
  - 使用する場合は、manifest.jsonに”content_scripts”と書いて値を設定
  - 「どこのページで」, 「どんなscriptファイルを実行するか」などを設定します
  - 制約がある(ChromeAPI群で使えないものがある,ページ内変数にアクセスできないなど)
- Background Page(Event Page)
  - バックグラウンドで実行されるjavascript
  - 使用する場合は、manifest.jsonに”background”と書いて値を設定
  - 制約がない
  - Background Pageは常にbackgroundで動くんで、Event Pageで必要な時に実行する方が良い