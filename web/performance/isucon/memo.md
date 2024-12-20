## sec 1

- **Web サービスは速ければ速いほどいい**
- Core Web Vitals
  - LCP
    - 2.5s でイエローカード
  - FID
  - CLS
- キャパシティ
  - 処理可能なスループットや同時接続数
  - 利用可能なリソース量
- クラウド時代
  - システムリソースの用意が柔軟（Elastic）に即時・随時可能（OnDemand）
- キャパシティの見積り方
  - 負荷試験
  - → パフォーマンスチューニング
- **きほんのき**
  - 推測せず計測する
  - 公平に比較する
    - apple to apple で比較
    - 意図的に変更したところ以外、同じ2つのデータを比較する
  - １つずつ比較する
  - **制約理論**
    - 全体のスループットはボトルネックのスループットに律速する
- **きほんのほ**
  - **速い Web サービスを作るのと、Web サービスを速くするのは根本的に違うアプローチ**
  - ボトルネックにだけアプローチする
  - ボトルネックの特定は外側から順番に
    - マクロ視点で全体を俯瞰
  - ボトルネック対処の３パターン
    - 解決、回避、緩和
- **きほんのん**
  - 負荷試験
    - 目的
    - シナリオ
    - 試行負荷
    - 試行回数
    - 試行時間
    - 実施期間

## sec 2

- モニタリング
  - **モニタリングは継続的なテストである**とも呼ばれている
    - 提供しているサービスが想定している形に動作しているかの確認という性質から
  - 『高速であること』を保証する
  - メトリクス
    - その時の状態を定量的に示した値
- モニタリング種類
  - 外形監視
    - ユーザーと同じ経路でアクセス
    - Synthetic Monitoring
    - SaaS:
      - https://ja.mackerel.io/
    - シナリオテスト
  - 内部監視
    - エージェント

``` sh
top -cd1
free --human

vmstat
sar
```

- モニタリングツール
  - Pull 型と Push 型
    - どちらのアーキテクチャでもエージェントが動作している
  - Prometheus はプル型
    - モニタリングアプリケーションがエージェントへメトリクスを要求・取得する
    - Pull 型の欠点を補う Service Discovery etc...
  - ツールよりも**何を対象にモニタリング**をするか
- https://www.nagios.org/
- **OpenMetrics**
  - Evolving the Prometheus exposition format into a standard.
    - https://www.cncf.io/projects/openmetrics/
  - **Prometheus が利用していたフォーマットを標準化したもの**
  - **エージェントの実装が非常に楽になり、さまざまなミドルウェア向けの exporter 開発が進んだ！**
- ベンチマーク
  - プロファイラ
    - ラインプロファイラ

## sec 3

### nginx

change log format

``` sh
sudo vim /etc/nginx/nginx.conf

# alp の使えるキーの名前に合わせる！
log_format json escape=json '{"time":"$time_iso8601",'
    '"host":"$remote_addr",'
    '"port":$remote_port,'
    '"method":"$request_method",'
    '"uri":"$request_uri",'
    '"status":"$status",'
    '"body_bytes":$body_bytes_sent,'
    '"referer":"$http_referer",'
    '"ua":"$http_user_agent",'
    '"request_time":"$request_time",'
    '"response_time":"$upstream_response_time"}';

# フォーマットを変更する
access_log  /var/log/nginx/access.log json;
```

validate format

``` sh
sudo nginx -t

sudo systemctl reload nginx
```

alp

``` sh
curl -OL https://github.com/tkuchiki/alp/releases/download/v1.0.21/alp_linux_amd64.tar.gz

tar -xvzf alp_linux_amd64.tar.gz
sudo mv alp /usr/local/bin/


cat /var/log/nginx/access.log | alp json

cat /var/log/nginx/access.log | alp json --sort=sum -r
cat /var/log/nginx/access.log | alp json --sort=avg -r
```

alp はデフォルトでは URI のクエリ文字列は無視して集計する。

### ab

Apatch Bench

単一の URL に対してリクエスト送信

``` sh
sudo apt update
sudo apt install apache2-utils -y

tail -n 10 /var/log/nginx/access.log | alp json -o count,method,uri,min,avg,max
```

### alb で解析するためのアクセスログのローテーション

``` sh
# 負荷試験のたびに実行する！
sudo mv /var/log/nginx/access.log "/var/log/nginx/access.log.$(date "+%Y%m%d%H%M%S")"
sudo nginx -s reopen


ab -c 1 -t 30 http://localhost/
```

### mysql

``` sh
cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep slow_query_log
```

- slow query log
  - https://dev.mysql.com/doc/refman/8.0/ja/slow-query-log.html
- **long_query_time を 0 にすると全てのクエリがログに出力される**
  - 1 回の大したことないクエリがいっぱい投げられてるとかもわかる

``` sh
$ cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep slow -C3
log_error = /var/log/mysql/error.log
#
# Here you can see queries with especially long duration
# slow_query_log                = 1
# slow_query_log_file   = /var/log/mysql/mysql-slow.log
# long_query_time = 2
# log-queries-not-using-indexes
#

sudo systemctl restart mysql
```


``` sh
# -t timelimit
ab -c 1 -t 30 http://localhost/

#  •   -s sort_type
#      ┌───────────────┬────────┐
#      │ Type          │ String │
#      ├───────────────┼────────┤
#      │ Default Value │ at     │
#      └───────────────┴────────┘

#      How to sort the output. The value of sort_type should be
#      chosen from the following list:

#      •   t, at: Sort by query time or average query time

#      •   l, al: Sort by lock time or average lock time

#      •   r, ar: Sort by rows sent or average rows sent

#      •   c: Sort by count

#      By default, mysqldumpslow sorts by average query time
#      (equivalent to -s at).
sudo mysqldumpslow -s t /var/log/mysql/mysql-slow.log
```

ヤバめなところを見てみる

``` sh
$ sudo head -n 30 /var/log/mysql/mysql-slow.log 

/usr/sbin/mysqld, Version: 8.0.36-2ubuntu3 ((Ubuntu)). started with:
Tcp port: 3306  Unix socket: /var/run/mysqld/mysqld.sock
Time                 Id Command    Argument
# Time: 2024-11-29T16:01:11.371757Z
# User@Host: isuconp[isuconp] @ localhost [127.0.0.1]  Id:     8
# Query_time: 0.000056  Lock_time: 0.000000 Rows_sent: 0  Rows_examined: 0
use isuconp;
SET timestamp=1732896071;
SET NAMES utf8mb4;
# Time: 2024-11-29T16:01:11.388965Z
# User@Host: isuconp[isuconp] @ localhost [127.0.0.1]  Id:     8
# Query_time: 0.017138  Lock_time: 0.000004 Rows_sent: 10001  Rows_examined: 20002
SET timestamp=1732896071;
SELECT `id`, `user_id`, `body`, `mime`, `created_at` FROM `posts` ORDER BY `created_at` DESC;
# Time: 2024-11-29T16:01:11.401053Z
# User@Host: isuconp[isuconp] @ localhost [127.0.0.1]  Id:     8
# Query_time: 0.001292  Lock_time: 0.000004 Rows_sent: 0  Rows_examined: 0
SET timestamp=1732896071;
# administrator command: Prepare;
# Time: 2024-11-29T16:01:11.419371Z
# User@Host: isuconp[isuconp] @ localhost [127.0.0.1]  Id:     8
# Query_time: 0.018294  Lock_time: 0.000001 Rows_sent: 1  Rows_examined: 100010
SET timestamp=1732896071;
SELECT COUNT(*) AS `count` FROM `comments` WHERE `post_id` = 10001;
# Time: 2024-11-29T16:01:11.419435Z
# User@Host: isuconp[isuconp] @ localhost [127.0.0.1]  Id:     8
# Query_time: 0.000005  Lock_time: 0.000000 Rows_sent: 1  Rows_examined: 100010
SET timestamp=1732896071;
# administrator command: Close stmt;
# Time: 2024-11-29T16:01:11.419516Z
```

`Rows_sent: 1  Rows_examined: 100010` これはやばい、10 万行スキャンして 1 行だけ返してる

``` sh
# pass: isuconp
mysql -u isuconp -p isuconp ;
```

``` sql
mysql> EXPLAIN SELECT COUNT(*) AS `count` FROM `comments` WHERE `post_id` = 10001;
+----+-------------+----------+------------+------+---------------+------+---------+------+-------+----------+-------------+
| id | select_type | table    | partitions | type | possible_keys | key  | key_len | ref  | rows  | filtered | Extra       |
+----+-------------+----------+------------+------+---------------+------+---------+------+-------+----------+-------------+
|  1 | SIMPLE      | comments | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 99666 |    10.00 | Using where |
+----+-------------+----------+------------+------+---------------+------+---------+------+-------+----------+-------------+
1 row in set, 1 warning (0.00 sec)


-- \G で形式変わるっぽい、は？
mysql> EXPLAIN SELECT COUNT(*) AS `count` FROM `comments` WHERE `post_id` = 10001\G
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: comments
   partitions: NULL
         type: ALL
possible_keys: NULL
          key: NULL
      key_len: NULL
          ref: NULL
         rows: 99666
     filtered: 10.00
        Extra: Using where
1 row in set, 1 warning (0.00 sec)

ALTER TABLE comments ADD INDEX post_id_idx(post_id);
```

### dstart

``` sh
sudo apt install dstat -y

dstat --cpu
```

## sec 4

### k6

- シナリオ可能
  - Cookie の解釈
  - 任意の HTTP ヘッダの設定
- プロトコル
  - HTTP/1.1, HTTP/2, WebSocket, gRPC

## sec 5

- MariaDB
  - MySQL から派生
- **NewSQL**
  - **一貫性と分散を両立**
    - c.f. NoSQL は一貫性を犠牲にして分散を実現。
  - いいな
    - https://www.climb.co.jp/blog_dbmoto/archives/5077
  - Cloud Spanner, TiDB, Cockroach DB

``` sql
mysql> SHOW PROCESSLIST;

+------+-----------------+-----------------+---------+---------+------+------------------------+------------------+
| Id   | User            | Host            | db      | Command | Time | State                  | Info             |
+------+-----------------+-----------------+---------+---------+------+------------------------+------------------+
|    5 | event_scheduler | localhost       | NULL    | Daemon  | 9087 | Waiting on empty queue | NULL             |
|   15 | isuconp         | localhost       | isuconp | Sleep   | 7370 |                        | NULL             |
| 7925 | isuconp         | localhost:47254 | isuconp | Sleep   | 1535 |                        | NULL             |
| 7927 | isuconp         | localhost:47272 | isuconp | Sleep   |  652 |                        | NULL             |
| 7928 | isuconp         | localhost       | isuconp | Query   |    0 | init                   | SHOW PROCESSLIST |
+------+-----------------+-----------------+---------+---------+------+------------------------+------------------+
5 rows in set, 1 warning (0.00 sec)



mysql> SHOW FULL PROCESSLIST;
```

### pt-query-digest

``` sh
sudo apt update
sudo apt install percona-toolkit -y

pt-query-digest --version

sudo pt-query-digest /var/log/mysql/mysql-slow.log
```

``` sh
MYSQL_PWD='isucon' mysql -u isucon -e "SHOW TABLES;" isuride


MYSQL_PWD='isucon' mysql -u isucon -e "SET GLOBAL slow_query_log = 1;" isuride
DATETIME=$(date "+%Y%m%d-%H%M%S")
MYSQL_PWD='isucon' mysql -u isucon -e "SET GLOBAL slow_query_log_file = '/var/log/mysql/mysql-slow-$DATETIME.log';"
MYSQL_PWD='isucon' mysql -u isucon -e "SET GLOBAL long_query_time = 0;" isuride

# 諸々の試験を行う。。。

# slow query log を閉じる。
MYSQL_PWD='isucon' mysql -u isucon -e "SET GLOBAL slow_query_log = 0;" isuride


sudo pt-query-digest /var/log/mysql/mysql-slow-20241208-024757.log


sudo pt-query-digest /var/log/mysql/mysql-slow-.log
pt-query-digest /var/log/mysql/mysql-slow-.log

ALTER TABLE `comments` DROP INDEX `post_id_idx`;
ALTER TABLE `comments` ADD INDEX `post_id_created_at_idx`(`post_id`, `created_at`);
```

``` sql
EXPLAIN SELECT COUNT(*) AS `count` FROM `comments` WHERE `post_id` = 10001 ORDER BY `created_at` DESC LIMIT 3\G
```

### Install Golang

``` sh
curl -LO https://go.dev/dl/go1.23.3.linux-amd64.tar.gz
# rm -rf /usr/local/go
sudo tar -C /usr/local -xvzf go1.23.3.linux-amd64.tar.gz
echo export PATH=$PATH:/usr/local/go/bin > ~/.bashrc
```


``` sh
sudo systemctl start isu-go
sudo systemctl enable isu-go


sudo systemctl restart isu-go
```

### ADMIN PREPARE

``` diff
-		"%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&parseTime=true&loc=Local",
+		"%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&parseTime=true&loc=Local&interpolateParams=true",
```

### IO 負荷が DB にかかってる場合

そもそもこれどう検知するのか

- データサイズの確認・Buffer Pool の活用
- バイナリログの向こうか
- ログのフラッシュタイミングの調整

## sec 6

- PHP, unicorn (Ruby)
  - マルチプロセス・**シングルスレッド**
  - プロセスあたり数十~数百 MB のメモリを消費
  - C10K 問題
- C10 K 問題の対策
  - goroutine
    - m:n スケジューリング
  - Java Virtual Threads
  - イベント駆動
    - nginx

``` sh
$ nginx -version
nginx version: nginx/1.24.0 (Ubuntu)


$cat /etc/nginx/nginx.conf
```

``` sh
# デフォルトは前方一致のため / だと全てのリクエストがマッチする。
$ cat /etc/nginx/sites-available/isucon.conf 
server {
  listen 80;

  client_max_body_size 10m;
  root /home/isucon/private_isu/webapp/public/;

  location / {
    proxy_set_header Host $host;
    proxy_pass http://localhost:8080;
  }
}

# static file は nginx で返すようにする。
server {
  listen 80;

  client_max_body_size 10m;
  root /home/isucon/private_isu/webapp/public/;

  location /css/ {
          root /home/isucon/private_isu/webapp/public/;
          expires 1d;
  } 
  location /js/ {
          root /home/isucon/private_isu/webapp/public/;
          expires 1d;
  }
  location / {
    proxy_set_header Host $host;
    proxy_pass http://localhost:8080;
  }
}
```

- ノンブロッキング I/O, 非同期 I/O
  - 非同期は通知が返ってくる
  - ノンブロッキングは自分でポーリングする
- 多重 I/O
  - 複数の FD を渡していずれかが I/O 可能になったら通知を受け取る
- nginx
  - ノンブロッキング I/O と多重 I/O を使っている
- **gzip 圧縮**
  - おおよそ 1/5 になるくらいの圧縮率がありそう
  - 小さいファイルだと逆に大きくなることも
  - **圧縮レベル**
    - Zlib のデフォルトの圧縮レベルは 6,
    - nginx の gzip_comp_level は 1~9 でデフォルトは 1
- **Brotli**
  - Google が 2015 に公開した圧縮アルゴリズム
  - **Web での利用を念頭において、Web でよく使われる単語が多く登録されている！**
- nginx
  - **デフォルトでは、アップストリームサーバーとのコネクションをつど切る設定**
    - キープアライブしたいなら HTTP/1.1 にするのと Connection ヘッダーを空にする

## sec 7

- インメモリキャッシュ
  - デメリット
    - デプロイ直後に Thundering herd problem が発生し、DB に負荷が集中しうる
      - nginx => proxy_cache_lock
    - アクセスが集中したなどが理由でスケールアウトさせる場合、キャッシュが存在しないサーバーを追加することで DB に負荷が増すなど、状況を悪化させる可能性がある
    - TTL の管理がむずい

## sec 8

- 外部コマンド
  - 多くの言語では外部コマンドを呼び出すとシェルを経由する
    - Go の exec.Command はシェルを経由しない
      - → 一般的な使い方であれば OS コマンドインジェクション脆弱性は発生しない
  - 言語特性
    - Go は正規表現エンジンが特徴で、ワンチャン遅い
- 冗長なログを出さない！
- HTTP Client
  - 同一ホストのコネクションを使い回す
    - Go 標準パッケージの http.Client はなるべく使い回す設定になっている
    - **Body の Close を忘れると TCP コネクションが再利用されない**
    - **Response の Read せずに Close すると TCP コネクションが再利用されない**
  - タイムアウト
    - DefaultClient はタイムアウトが設定されていない

## sec 9

- カーネル
  - ユーザーランドからシステムコールでカーネルにリクエストを送る
- PID
  - Process ID
  - init
  - `ps auxfww`
- Linux のネットワーク
  - Linux NAPI
    - **できるだけ割り込み命令を減らしながら遅延の少ない形でパケットを処理したい！**
    - 割り込み命令 + ポーリング
- ストレージ
  - fio
- cpu
  - top
    - `top -1`
      - 各 core ごとの使用率がわかる
    - `us`
      - ユーザー空間の cpu 使用率
    - `sy`
      - システム空間の cpu 使用率
      - TLS の複号化など
    - `wa`
      - IO wait
- ulimit
  - **プロセス単位で設定されている**
- mtu
  - Ethernet に由来した 1500 byte が長らく使われてきた
  - 刻むほど効率は悪いので 9000 byte が使われることもある
    - **Jumbo Frame**
  - `ip link`
  - `ip link show ens3`

## そのほか

``` sh
.
├── backup
│   └── mysqldump.sql.bz2
├── env.sh
└── private_isu
    ├── benchmarker
    │   ├── bin
    │   ├── cache
    │   ├── checker
    │   ├── cli.go
    │   ├── cli_test.go
    │   ├── Dockerfile
    │   ├── go.mod
    │   ├── go.sum
    │   ├── main.go
    │   ├── Makefile
    │   ├── run.sh
    │   ├── scenario.go
    │   ├── score
    │   ├── sql
    │   ├── userdata
    │   ├── userdata.go
    │   ├── util
    │   └── version.go
    ├── LICENSE
    ├── Makefile
    ├── manual.md
    ├── public_manual.md
    ├── renovate.json
    └── webapp
        ├── docker-compose.yml
        ├── etc
        ├── golang
        ├── node
        ├── php
        ├── public
        └── ruby
```

## Appendix

``` sh
./bin/benchmarker -u ./userdata -t http://52.195.230.121
```
