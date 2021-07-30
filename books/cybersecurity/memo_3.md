# 第三部
bashによるペネとレーションテスト

## sec 13
- ftp(File Transfer Protocol), ftpコマンド
  - FTPサーバとの間でファイルを転送するために用いられる
  - デフォルトではTCPポート21を用いて接続される

```sh
# port num 50hh[]
$ ftp 192.168.6.15 50
```

### curl
- -L: ページのURLがリダイレクトされた際の追跡を行う設定ができる
- -o: ファイルに書き込むことができる
  - `curl -o output.html https://www.oreilly.com`
- -I: サーバからのヘッダ情報を取得することもできる

```sh
$ curl -LI https://www.oreilly.com
$ curl -LIs https://www.oreilly.com | grep 200
```

サーバに接続すると、WebサービスのアプリケーシンやOSに関する幾つかの情報が確認できることがある。これをバナーと呼ぶ！

