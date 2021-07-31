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


## sec 14
可読性は大半のアプリケーションにとって望ましいことではあるが、ペネとレーションてすとの実行においてはその限りではない。

- 難読化
  - 文法の難読化
  - ロジックの難読化
  - エンコードもしくは暗号化

base64

```sh
$ echo 'Rapid Cybersecurity Ops' | base64
UmFwaWQgQ3liZXJzZWN1cml0eSBPcHMK

# -d: decodeする
$ echo 'Rapid Cybersecurity Ops' | base64 | base64 -d
Rapid Cybersecurity Ops
```

### eval
与えられた引数を現在のシェル内で実行する。

スクリプトないで動的にシェルコマンドを生成する場合等に有利である

### openssl
```sh
openssl aes-256-cbc -base64 -in innerscript.sh -out innerscript.enc -pass pass:mysecret
```

### read
入力を受け取る

-sオプションをつけることで、入力が画面に表示されなくなる

```sh
$ read -s word
```

### shift
shiftにより、引数が削除され、次の引数があれば、それが先頭の引数$1として参照されるようになる


## sec 15
ファジングは、実行ファイル、プロトコル、システムなどに内在された潜在的な脆弱性を特定するために用いられる手法である。

## sec17
```sh
# ACLなどを確認するコマンド

$ getfacl fd2.sh 
# file: fd2.sh
# owner: ubuntu
# group: ubuntu
user::rw-
group::r--
other::r--
```

## sec18
ログの書き込み

適切なログエントリの条件

- 一貫した命名規則及び構文が使われている
- コンテキスト（Who, Where, When）が記述されている
- 具体的である（What）

方法

- eventcreate（windows）
- logger(linux)

### logger
- syslogにイベントを書き込む際に用いられる
- 通常/var/log/messagesに格納される
  - systemにより異なる
  - ラズパイのubuntuでは、/var/log/syslog

```sh
$ logger 'This is an event'
```

## sec19

### ping
pingコマンドはICMP(Internet Cntrol and Messaging Protocol)を用いてリモートのシステムが利用可能かどうかを確認する

> ICMPトラフィックはネットワーク上のファイアウォールなどの機器によってブロックされていることがある。機器へのpingが無反応だった場合に、機器が稼働していないと決めつけてはいけない。ICMPパケットがフィルタされていただけということもありうる。

pingを通して、起動確認

```sh
$ bash pingmonitor.sh monitor.txt 10
```



