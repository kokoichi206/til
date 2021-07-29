## sec5
データとは、ほぼ全ての防御のためのセキュリティ活動における生き血である。

cut

```sh
$ cut -d' ' -f2 cutfile.txt
```

fileコマンド

fileコマンドは、ファイル名だけでなく、マジックナンバーと呼ばれるファイルの先頭部を読み込み解析する

```sh
$ ssh myserver ps > /tmp/ps.out
$ ssh ubuntu@192.168.3.7 ls > ls_out

# リモートシステムのファイルにリダイレクトするには
$ ssh .... \> ./tmp.out

# ローカルシステムのスクリプトをリモートで実行！
$ ssh myserver bash < ./osdetect.sh
```

/var/log以下のログファイルをまとめる！

```sh
$ tar -czf ${HOSTNAME}_logs.tar.gz /var/log/

# オプション
# -c: アーカイブファイルの作成
# -z: ファイルの圧縮
# -f: ファイル名の指定 
```

- 重要なログファイル
  - /var/log/auth.log
  - /var/log/kern.log
    - カーネルのログ
  - /var/log/messages
    - 致命的でないシステム情報
  - /var/log/syslog
    - 汎用的なシステムのログ

| Linuxコマンド | 目的 |
| --- | --- |
| uname -a | OSのバージョン情報 |
| cat /proc/cpuinfo | システムのハードウェア情報 |
| ifconfig | ネットワークインタフェース |
| route | ルーティングケーブルの表示 |
| arp -a | ARPテーブルの表示 |
| netstat -a | ネットワーク接続の表示 |
| mount | ファイルシステムの表示 |
| ps -a | 実行中プロセスの表示 |


find

```sh
$ find /home -name "*password*"
# -inameにすると大文字小文字区別しない

# 隠しファイルの検索
$ find /home -name '.*'

$ find /home -size +5G

$ find / -type f -exec ls -s '{}' \; | sort -n -r | head -5
```

!! のコマンドで、最後に実行されたコマンドを呼び出すことができる！！


## sec6
CSV, JSON, XMLの解析ができるようになる

```sh
# tail -n +2で、2行目からの出力を行う
$ cut -d',' -f1 csvex.txt | tr -d '"' | tail -n +2
```

<span style="color:red">
複数行にわたる、XMLやHTMlの検索！
</span>

```sh
# -z: 改行文字を一般の文字と同じように扱う
# -P: (?s),パール固有のパターンマッチで、メタもじ.が改行にもマッチするようになる
$ grep -Pzo '(?s)<author>.*?</author>' book.xml
```


## sec7
```sh
$ cat file1.txt
12/05 192.168.10.14
12/25 192.168.10.185

# ２番目のオクテットだけでソート
$ sort -k 2.5,2.7 file1.txt
```

Webアクセスろぐの解析
```sh
$ awk '$9 == 404 {print $1}' access_log | bash countem.sh

$ cut -d' ' -f 1,10 access_log | bash summer.sh | sort -k 2.1 -n

$ cut -d' ' -f1,10 access_log | bash summer.sh | bash histogram.sh

$ bash pagereq.sh 45.146.164.110 < access_log | sort -rn

$ bash useragents.sh < access_log
```

ユーザーエージェント文字列

式評価で正規表現を用いたい！

- if文はブラケット（大カッコ）を二重にする
- 演算子は"=~"
- 正規表現はクォーテーションで括らない（正規表現で特別扱いの文字がバックスラッシュでエスケープされるため）
- 後方参照（カッコで囲った部分）は ${BASH_REMATCH[1]} で取得（複数ある場合、[2][3]…で取得）

```sh
#!/bin/bash
 
foo=abc123efg
 
if [[ ${foo} =~ ^[a-z]+([0-9]+).*$ ]]; then
    echo ${BASH_REMATCH[1]}
fi
```

```sh
# オプションをつけたりした

$ cut -d' ' -f1,10 access_log | bash summer.sh | bash histogram.sh -s 25

$ bash useragents.sh -f testtest < access_log
```


## sec8
監査ログの維持、監視、分析（maintenance, Monitoring, Analysis）

ログをリアルタイムに監視するもっとも基本的な方法は、`tail -f`である

```sh
$ tail -f /var/log/apache2/access.log
$ tail -f /var/log/apache2/access.log | egrep -i 'HTTP/.*" 404'

$ tail -f /var/log/apache2/access.log | egrep --line-buffered 'HTTP/.*" 404' | cut -d' ' -f4-7
```

コマンドラインのバッファ

> I/O呼び出しは非常に「高価（時間を要する）」ので、なるべく削減した方がプログラムの効率は向上する。そこで、grep系のプログラムでは、マッチする行を見つけた際に、その行をバッファと呼ばれる広大なメモリ領域に格納する


[IOC(Indicator of Compromise)](https://www.logsign.com/blog/what-is-ioc-in-cyber-security/)

```sh
# in ioc.txt
# ディレクトリとラバーサル攻撃
\.\./

# -f: pattern file
$ tail -f /var/log/apache2/access.log | egrep -i -f ioc.txt
```

looper.sh

```sh
shopt -s lastpipe

# パイプラインを構成する最後のコマンドを、スクリプト自身と同じプロセスで実行する！
# 通常は、パイプラインのコマンドはサブシェルで実行される！

tail -f --pid=$$
# tailがパイプラインに残ったままにならないよう、
# 指定したpidの死亡と同時に、自身も殺すオプション

# 置換演算子？
# ${varname:-word}	 
# varname が存在し NULL ではない場合， その値を返す．それ以外は，word を返す．
```

tailcount.sh

```sh
# HOW TO USE?
$ bash tailcount.sh access_log 
$ bash tailcount.sh access_log | bash livebar.sh

trap cleanup EXIT
# EXITはシグナルではなく、trap構文の特殊ケース

# $!, $はパラメータ展開をしている
# ! 最後に実行されたバックグラウンド (非同期) コマンドの プロセス ID 
# 調べるところ：
# http://linuxjm.osdn.jp/html/GNU_bash/man1/bash.1.html
```


## sec9
ネットワーク監視

Nmap Ndiffなどでも同様のことが可能

```sh
$ crontab
# option
# -e: cronテーブルを編集する
# -l: cronテーブルを一覧する
# -r: cronテーブルを削除する

## windでは schtasks で行える
```

ポートスキャナの作成

TCP接続を特定ホストの特定ポートに行うことができればよい

`/dev/tcp`というbashのファイルディスクリプタを用いると実現可能

システムコールstrftime

```sh
$ man strftime
```

printfは`-v`をつけると、出力の代わりに変数に格納される

```sh
$ printf -v TODAY 'scan_%(%F)T' -1
```

`/dev/tcp`など、存在しない？

```sh
# 以下のようなコマンドで調べると良い？これはbashの機能
$ man bash | grep tcp -C15
```


新規にポートがオープンもしくはクローズしたことを確認できたら、それが適切な変更か、悪意を持った活動の兆候かを確認する


2つの異なるストリームからの読み取りのために、ファイルディスクリプタ4,5などを用いる

```sh
# &をつけることでファイルディスクリプタを表す
read aline <&4 || break     # at EOF
```

