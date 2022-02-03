# Practical Data Science & Engineering Vol.1

## sec 1
世の中には簡単な法則で成り立っている事象と、複雑でカオス的な振る舞いをする事象の２つに大きく二分できる。

カオス的な振る舞いは簡単な法則性が背景にあると仮定し、法則性を見つけ出そうとすると、思わぬ落とし穴にはまることがある。

定量化、つまりデータを大量に束ねて「**大きな数にすることで真実が初めて見えてくる**」

## sec 2
requests では、html の情報取得のリクエストを投げるだけで、js の解釈はしてない。つまり、**jsが動くことで初めて描画されるようなコンテンツに関しては、検知することができない**

サイト側の対策としては、js でラップすることで、簡単には解析させないようにする。

そこで、google chrome + selenium のでばん

32.1: 公表された著作物は、引用して利用することができる。

### ハイパーリンクが作るネットワークは探索問題
kvs などのキー（URL）に対して、O(1)の計算量でデータを引き出せるアルゴリズムが適している。

#### 探索方式
- 幅優先探索
    - 浅い領域を優先してスクレイピングを継続
- 深さ優先探索
    - 深い方を優先して探索
    - 最初に設定した URL から遠く深いところを優先してスクレイピング
- ビームサーチ
    - 幅優先探索と深さ優先探索のバランスをとった方法
    - 一定の探索幅を維持して、深さも幅も良いとこどりをする


## sec 3
エンピリカルには、MySQLやPostgressSQLを用いるより、KVSなどのより速度と非構造化データ（リレーショナル性が低いデータ）に対して、有効。

スクレイピングデータはHTMLなどはパースしてきれいに整形すれば、RDBなどと相性がいいが、本格的なパースや整形は後で行い、データを集めることを最初に行うとすると、KVSが相性が良くなる。

### KVS
LevelDB, RocksDB などがあるが、マルチプロセスでのプロセス間を横断したアクセスができない！

逆に疎結合を意図したRBDのインターフェースなどはこの制約を受けないが、KVSと比較した時に速度が極めて遅くなる。

### 最強のDBは結局ファイルシステム
ファイルシステムはOSやファイルを格納するしあのSSDやHDDの、一定のルールで書き込み読み込みを制御するデータの格納ルール。

WindowsのNTFS, MacOSのApple File System, Linuxのext4など

いずれのファイルシステムも一長一短がある

ファイルシステムは特定のキーに対して、計算量O(1)でアクセスできるので、実質KVSとして動作できる。

namedtuple という、scala か kotlin などの DataClass に相当するものがある！シリアライズもサポートしている！

`concurrent.future.ProcessPoolExecutor`は、引数に与えた関数をマルチコアで動作させるライブラリ

> よく作られたKVSのライブラリを選択するより、ファイルシステムをうまく使用してKVS Likeなことを作った方が結果として安定性もスケールアウト性も優れており、最終的に並列処理が伴うようなプログラムを作る際、このような方法に落ち着くことが多い！！


## sec 4
Depth 1, UserAgent, Refferer を偽装する

``` python
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
r = requests.get('https://www.yahoo.co.jp/', headers=headers)
```

### 自分のUserAgent
Google で、"my useragent"と入力する！

### サイト管理人格に配慮する
UserAgentやIPなどは、基本的にアクセスログとして残る。

以下のように、これが誰かのスクレイパーであること、サポートを得るためのURLを載せるなどすることがあり、意図しないアクセスであっても、穏便に済ますことができる

``` python
import requests

headers = {
    'User-Agent': "ozilla/5.0 (Linux; Analytics2) [This is a scraper of nardtree's analytics. https://gink03.github.io]"
}
r = requests.get('https://www.yahoo.co.jp/', headers=headers)
```

### Referrer を偽装する
現在、Referrer の要素がクローラーかどうかを判断する要素にはならないが、昔からあるレガシーなクローラーを弾く作法の１つに、Referrer で判断するサイトもある

``` python
import requests

headers = {
    'referer': 'https://google.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}
r = requests.get('https://www.yahoo.co.jp/', headers=headers)
```


## sec 5
IP を偽装する

最近の Google 社のサービスや、GAFA などの強いプレイヤーのサービスは ML による異常なアクセスを行うユーザの BAN が行われるようになってきている。

今も現在もおそらく一番の不正利用のシグナルは IP アドレス

### プロキシサーバを立ててアクセス
最も簡単なのが何らかのクラウド業者に Linux のインスタンスを借りて、プロキシサーバを立てて、そこ経由でアクセスすること

`squid`など。

``` bash
$ docker run -d -p 3128:3128 nardtree/squid

# 133.130.97 はインストールしたサーバのグローバル IP アドレス
$ curl --proxy http://user:user@133.130.97:3128/ https://ifconfig.co/
$ curl https://ifconfig.co/
```

クラウド業者もそんなことやられたら困るので、対策されている。。。

``` python
# proxy の例
import requests

proxies = {
    "https": "http://user.user@133.130.97:3128/",
    "http": "http://user.user@133.130.97:3128/"
}
r = requests.get('https://ifconfig.co/', proxies=proxies, verify=False)

print(r.text)
```

### 公開プロキシ経由でアクセス
Proxy サーバ自体は多くの人にいろんな政治的・思想的理由があり、それを補助するためにあらゆる地域と国家で建てられている。

[spys.one/en](https://spys.one/free-proxy-list/JP/)では、ロシアのサーバにさまざまな proxy が公開されている。

### tor 経由でのアクセス
tor 経由でアクセスするとほぼ通信元が辿れなくなるという匿名性がある。

``` bash
# server
$ docker run -d --restart=always -p 0.0.0.0:9150:9150 peterdavehello/tor-socks-proxy:latest
# client
$ curl --socks5-hostname 119.106.0.95:9150 https://ipinfo.tw/ip
```

うまくいかなかった。。。

```
curl --socks5-hostname 119.106.0.95:9150 https://ipinfo.tw/ip
curl: (7) Failed to connect to 119.106.0.95 port 9150: Connection refused
```

この IP を `whois` で確認すると（どうやって？）

``` python
# pip install "requests[socks]"
import requests
proxies = dict(http='socks5h://133...:9150',
            https='socks5h://133...:9150')
r = requests.get('https://ipinfo.tw/jp', proxies=proxies)
print(r.text)
```


## sec 6
MultiCore, Multi Machine でスクレイピング

大量のCPUのコアを効率的に使える標準ライブラリ

- concurrent.futures.ProcessPoolExecutor
    - マルチプロセス
- concurrent.futures.ThreadPoolExecutor
    - GILというレガシーな仕組みを使ったスレッド
- asyncio
    - ノンブロッキングIO

マルチプロセスは、forkという機能を使って実現しているプログラムのOSから見る実態を増やす。この時メモリに重なる部分が多いので消費を低減して、実態を複数個作る。forkで新たに作られた子プログラムと親プログラムは原則として何らかのサイクをしない限り通信できない

マルチスレッドは、１つのプログラムの中で、CPUリソースを割り当てを変えながら同時に２つ異常動作させる仕組み。このCPU割り当てスケジューリングには多くの手法があり、ioがブロックされている間は別の処理をするようにしたものがasyncioが行うスレッド

|| MultiProcess | Thread |
| --- | --- | --- |
| メモリ効率 | 悪い | 良い |
| 速度 | 良い | 悪い |
| 共有変数のシンク | 原則できない | できる |

### MultiprocessingをMulti Machineに拡張
Multiprocessingは原則としてプロセス間でメモリ内容の共有ができない

PIPEやhttp通信やファイルシステムをバイパスすれば、これらの制約は回避することができる

例えばデータをホストするマシンを一台用意し、nfsやsshfsなどで、リモートのマシンのフォルダーやハードディスクを共有すると同時に並列にアクセスできる。


## sec 7
フェアネスを考慮したスクレピング

過負荷を防ぐ方法

### ランダムドメイン選択
全てのドメインに対して平等なスクレイピングの機会を与える方法

`server-clientモデル`

#### server
serverでは、オンメモリでdomainとURLのSet情報の対を持っていて、domain粒度でfairnessをコントロールすることで、実際にScrapingを行うclientにどのURLをスクレイピングしていいかを通知する。


