## sec 0
ISUCON = Iikanjini Speed Up CONtest

## sec 1
高速であること、は現代の Web サービスの必須条件（かつては達成できているとベターな条件だった）

Google -> Core Web Vitals という指標をもとに検索順位を考慮している。

RTT(Round Trip Time) にかかる時間が短いサービスのことを、高速なサービスと定義する。
同時並行処理性能（スループット）も考慮して高速化を図る（rps: requests per second）

「負荷が高い」＝「システムリソースのうち、短時間で利用量が大きく変わる、時間流動性が高いシステムリソースの利用率が高い状態」

キャパシティ＝個々の性能×数
個々の性能を高める＝垂直スケーリング：スケールアップ
数を増やす＝水平スケーリング：スケールアウト

**推測せず計測する**

TOC: Theory Of Constraints
全体のスループットはボトルネックのスループットに律速する。

速い Web サービスをつくるのと、Web サービスを速くするのは根本的に違うアプローチ！
実際のサービスの場合は、ボトルネックとなる部分の利用ユーザーが少なければそこを削除するのがいいことも！

**ボトルネックだけにアプローチする**
システムリソース 100% が必ずしも悪いことではない。

ボトルネックの箇所の特定ができたら、マクロからミクロへのアプローチに切り替え、原因の推定を行う！

- 解決
- 回避
- 緩和

パフォーマンスチューニングの具体的活動は、負荷試験⇨改善⇨負荷試験、、、を繰り返すこと。

お金は等価交換可能なリソース。
時間や機会のような等価交換不可能なリソースの獲得にお金を投入するのはいいことでもある。


## sec 2
**モニタリングは継続的なテスト**であるとも言われる。

レイテンシなど、その時の状態を定量的に示した値のことを**メトリクス**という。メトリクスの時系列で可視化したものはモニタリンググラフなどと呼ばれる。
重要なのは、一貫した変わらない視点でモニタリングすること！

top command
id = idle

CPU に負荷をかけるコマンド！？
stress --cpu 2

vmstat, dstat, sar


[prometheus](https://prometheus.io/)はモニタリングツールの１つ

[node_exporter](https://github.com/prometheus/node_exporter)は、Prometheus 向けに開発された Linux におけるリソース取得エージェント。

モニタリングサービスのアーキテクチャとして、プル型とプッシュ型がある。プッシュ型の方がマルチサービスではメリットが大きい。

Prometheus はプル型のアーキテクチャが採用されているが、その欠点を補うような機能やエコシステムが魅力。

node_exporter は Linux ホスト１台につき１つインストールされる。

``` sh
# 現在使用している port を調べる
$ sudo lsof -i -P -n


wget https://github.com/prometheus/prometheus/releases/download/v2.36.2/prometheus-2.36.2.linux-amd64.tar.gz
ls
tar xvfz prometheus-2.36.2.linux-amd64.tar.gz
ls
cd prometheus-2.36.2.linux-amd64/
ls
sudo vim prometheus.yml
   53  vim prometheus.yml
   54  sudo apt install vim
   55  vim prometheus.yml
   56  ./prometheus --config.file=prometheus.yml
   57  netstat
   58  lsof -i
   59  vim prometheus.yml
   60  ./prometheus --config.file=prometheus.yml
   61  vim prometheus.yml
   62  sudo lsof -i -P -n | grep 9090
   63  sudo lsof -i
   64  sudo lsof -i -P
   65  sudo lsof -i -P -n
   66  history
```

``` sh
./prometheus --config.file=prometheus.yml --web.listen-address=:9091
./prometheus --config.file=prometheus.yml --web.listen-address=:8080 &

# access
http://192.168.0.5:9091/metrics
curl http://192.168.0.5:9091/metrics
```

prometheus の出力は [OpenMetrics](https://openmetrics.io/) と呼ばれる標準化されたフォーマットに沿ったものとなっている。

``` sh
# wifi メトリクスの取得
./node_exporter --collector.wifi
```

avg without(cpu) (rate(node_cpu_seconds_total{mode!="idle"}[1m]))


負荷試験への考え方: [RFC 2544 - Benchmarking Methodology for Network Interconnect Devices 日本語訳](https://tex2e.github.io/rfc-translater/html/rfc2544.html)


ログに対するモニタリング



## sec 3
性能を数値化するための負荷試験を実行するソフトウェアをベンチマーカー。

[private-isu](https://github.com/catatsuy/private-isu)

- OS として Ubuntu Linux
- データを保存する RDBMS として MySQL
- セッション管理のストレージとして memcached
- Web サーバー兼リバースプロキシとして nginx

curl -L -O https://github.com/catatsuy/private-isu/releases/download/img/dump.sql
.bz2

負荷しけんの測定方法。
Web サービスに負荷を与えるベンチマーカー側で計測する方法と、負荷を与えられる Web サービス側で計測する方法がある。

負荷試験中以外であっても、Web サービスの性能をサーバー側で計測できるようにしておくことは大変重要！！

``` sh
log_format json escape=json '{"time":"$time_iso8601",'
                            '"host":"$remote_addr",'
                            '"port":"$remote_port",'
                            '"method":"$request_method",'
                            '"uri":"$request_uri",'
                            '"status":"$status",'
                            '"body_bytes":"$body_bytes_sent",'
                            '"referer":"$http_referer",'
                            '"ua":"$http_user_agent",'
                            '"request_time":"$request_time",'
                            '"response_time":"$upstream_response_time"}';

server {
  listen 80;

  client_max_body_size 10m;
  root /public/;

  location / {
    proxy_set_header Host $host;
    proxy_pass http://app:8080;
  }

  access_log /var/log/nginx/access.log json;
}
```

nginx のログを変更したあと。

```
excape=json{"time":"2022-06-30T21:40:41+00:00","host":"172.27.0.1","port":"57114","referer":"http://localhost/","request_time":"0.096","response_time":"0.096"}
```

JSON 形式のアクセスログの集計。alp を使う。
alp は短期的なログの解析には便利だた、長期的なログ（実運用）には向いてない

```
brew install alp

cat access.log | alp json
alp json --file access.log
```

Apache HTTP Server に付属する ab コマンド（Apache Bench）！

mac には標準でついてる。

``` sh
# ubuntu
apt install apache2-utils
```

``` sh
ab -c 1 -n 10 http://localhost/
ab -c 1 -n 30 http://localhost/
```

アクセスログのローテーション

負荷試験施行のたびに行うのを忘れない。

``` sh
#!/bin/sh
set -eu

mv /var/log/nginx/access.log /var/log/nginx/access.log.$(date +%Y%m%d-%H%M%S)
# nginxにログファイルを開き直すシグナルを送る
nginx -s reopen
```

requests per second を指標として使う。


スロークエリログの設定。
パフォーマンスチューニングにおいては long_query_time を 0 に設定して、全てのクエリのログを記録するのがおすすめ。


サーバーの処理能力を使い切れているかの確認。
なぜ CPU を使い切れていないのか。
unicorn は、１プロセスで１リクエストを処理するアーキテクチャになっている。


CPU によっては、同時マルチスレディング（Simultaneous Multi-Threading, SMT）というアーキテクチャが採用されていることも。


