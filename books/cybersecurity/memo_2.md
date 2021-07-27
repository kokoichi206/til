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

