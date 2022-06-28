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






