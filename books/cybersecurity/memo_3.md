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

## sec20
組織内でどのようなソフトウェがインストールされているかを理解することは、ネットワークのセキュリティを維持する上で重要なステップである。この情報は環境に対する理解を深めるだけでなく、アプリケーションのホワイトリスト化といった、より高度なセキュリティ制御を行うために用いることもできる。

パッケージ管理ツールを通してインストールされたものに関しては、softinv.shで行っている

script

```sh
$ col -bp < 20210731.log | sed 's@^0;@@' | sed 's@01\;[0-9]*m@ @g' | awk '{if($1 == "ubuntu@ubuntu:"){{printf("%s%s$ ",$1,$2)}{for(i=5;i<NF;++i){printf("%s ",$i)}}{print $NF}}else{print $0}}'
```

まずターミナル上にエスケープシーケンスを表示させるために、`col`コマンドを使っています。
その上で、表示された文字を眺めながら以下の３つの処理を行いました
1. 先頭の「0;」を削除する
2. 途中で現れる「01;32m（色の情報？？）」などをスペースに変換する
3. コマンド入力ラインは情報がダブってたので、ダブりを削除
それぞれの処理が各パイプラインの処理に対応してます



## Appendix
```sh
$ echo aaa > /dev/tcp/localhost/80
$ echo $?
0
```

### bashのトレースオプション
bash実行時に、「何を実行しているか」を確認する

- スクリプトの先頭で、#!/bin/bash -x と指定して実行
- スクリプト実行時に、`bash -x [filename]`というようにして、当該スクリプト実行時にトレース結果を表示するように指定する。
- トレース結果の出力先は、標準エラー出力である。



