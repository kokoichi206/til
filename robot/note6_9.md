## ファイルシステム
- OSの最重要機能の一つ
- 機能
    - 誰にでもわかりやすいもの
        - HDDを使えるようにする
        - USBを使えるようにする
    - 人によっては意外なもの
        - 外部の機器（センサ等）を使えるようにする
        - OSと通信する

### ローカルファイルシステム
- 主なファイルシステム
    - ext4, ext3, (extended file system): Linux
    - UFS2 (Unix File System2): FreeBSD
    - APFS (Apple File System), HFS+: Mac OS
    - NTFS (NT File System), FAT16, FAT32, exFAT: Windows
- 特殊なファイルシステム
    - procfs, sysfs, tmpfs, スワップファイルシステム

- ストレージの区分け（上位レイヤーから順に）
    - パーティション
    - ローカルファイルシステム
    - ブロックグループ
    - ブロック

```
sudo parted -l
```
Partition Table: msdos
なのは面白い。

```
df -Th | grep -e Filesystem -e mmc
sudo dumpe2fs -h /dev/mmcblk0p2 | grep -i block | head
ls -i
```
ブロックのサイズが4096バイト
これがちっちゃすぎると、データがこまぎれになって、読み込むのに時間がかかってしまう。
- iノード番号がファイルの本体を表す番号全て！
```
ln hoge hoge2
ls -i
```

ディレクトリもファイルなのでiノード番号を持つ

### 仮想ファイルシステム
- 主な役割：ローカルファイルシステムの違いを吸収
    - iノードという概念がないローカルファイルシステムもiノードをなんとか実現
- 機能
    - メモリ上にiノード（iノード構造体）やディレクトリエントリ（dentry構造体）を展開してユーザプログラムとやりとり
    - データブロックの内容をメモリ上に保持（キャッシュ）

 
```
time seq inf | head -n 10000 > /dev/null
```

### デバイスドライバ
- デバイスドライバ
    - 計算機に接続された機器を操作するためのプログラム
    - HDD、ディスプレイ、カメラ、マイク、端末、...
- バイスファイル
    - デバイスドライバのインタフェース
    - ファイルとして表現されている

- カーネルの一部として動作
    - Cで言えばmainを持たない関数の塊
    - 本来はカーネルと同時にコンパイルされるべき
        - ただしそれをやってしまうと時間や手間の無駄
- Linuxにはカーネルの一部を動的に脱着する仕組みが存在
    - カーネルの一部：カーネルモジュール（拡張子 .ko）

### カーネルモジュールの調査
- ファイルの検索
    - sudo find / | grep '\.ko$'
    - 今使われているカーネルモジュールは lsmod で調査
        - lsmod | less
        - lsmod | grep blue


## LED
- 回路の例
    - GPIO25とGNDの間にLEDを接続
        - GPIO25: 22番ピン（下の左から10番目）
        - GND: 39番ピン（上の一番左）
        - LEDのアノード（足の長い方）をGPIO25に
- 抵抗を使う場合は200-300Ω程度つないだほうがいい

### sys での光らせ方
```
cd /sys/class/gpio/
sudo -s
echo 25 > export 
ls
cd gpio25
echo out > direction 
echo 1 > value 
echo 0 > value 
echo 25 > unexport
exit
```
ここからはデバイスドライバ（デバドラ）を書く

### デバイスドライバ
OSの一部として動く
巨大なCであるカーネルに、新たに関数をぶち込むだけ
カーネルモジュール

### Makefile
- myled.ko: myled.c がカーネルモジュール
- Makefileを作った後 make を実行する

### Makefile, make
- 処理の手順を書いたファイル
    - コロンの左側をターゲットという
        - 作りたいファイルか、任意の処理名
- リナックスのヘッダーを使って、.cファイルのコンパイルをして、カーネルモジュールを作ってくれる
- make: Makefileを実行するためのコマンド
    - make clean もある

### カーネルモジュールの｛イン、アンイン｝ストール
```
echo {in,unin}stall
```
- インストール
    - insmodでインストールできる
    - /dev/等にはまだ何も出てこない
- アンインストールと後始末
    - rmmod

```
sudo insmod myled.ko 
lsmod | grep myled
sudo rmmod myled
```

### ログを吐くようにする
- init_modとclenup_modに「printk」という関数を追加
    - printf等stdio.hの関数は使えない
        - カーネルの中では動かない
    - こうやってログに残す
- 補足
    - KERN_INFO: ログのレベルを示すマクロ
    - __FILE__: ソースコードのファイル名

### 名前等を追加
- modinfo myled.ko

### デバイス番号の取得
- unregister_chrdev_region: デバイス番号の解放
    - 引数: dev、マイナー番号を1個返す
    - これを怠るとinsmodのたびに番号が増えていくので実験すると面白い
```
tail -n 1 /var/log/kern.log
```

### キャラクタ型デバイスを作る
- キャラクタデバイスの情報を格納する構造体 static struct cdev cdv:
- キャラクタデバイスの挙動の記述と登録
    - led_write: デバイスファイルに書き込みがあった時の挙動
    - static struct file_operations lef_fops: 挙動をカイタ関数のポインタを格納する構造体
        - VFSから使われる
- カーネルの恐ろしいところはみすると止められなくなる、再起動しか無い
    - 普段、カーネルに守られている
- cdev_init: キャラクタデバイスの初期化
    - file_operationsを渡す
- cdev_add: キャラクタデバイスをカーネルに登録

### 動作確認
- sudo mknod /dev/myled0 c 507 0 でデバイスファイルを手動作成
    - c: キャラクタデバイス
    - 507: メジャー番号（場合により変わる）
    - 0: マイナー番号
```
sudo mknod /dev/myled0 c 507 0
sudo chmod 666 /dev/myled0 
ls -l /dev/myled0 
echo abc > /dev/myled0 
tail /var/log/kern.log 
sudo rm /dev/myled0 
```

### クラスの作成と削除
- /sys/class 下にこのデバイスの情報を億
    - ユーザ側から情報が見えるように
- class_create で作成 
    - THIS_MODULE: このモジュールを管理する構造体のポインタ

ちゃんとファイルはできている
```
ls -l /sys/class/myled/
```

```
cd /sys/class/myled/
ls -l
cd myled0
ls
cat dev
```

- udevというサービスが/sys/class/myled/myled0/devをみてデバイスファイルを作成

### デバイスファイルからの字の読み込み
- カーネルの外（ユーザランド）からの字を取り込む
    - copy_from_userという関数を使用

### 最終LED
```
make
sudo insmod myled.ko
sudo chmod 666 /dev/myled0
echo 1 > /dev/myled0 
echo 0 > /dev/myled0
```

### まとめ
- デバイスドライバのコードを書いた
- VFSのread,writeを実装
    - 疑似ファイルの入出力を実装
- udev
    - デバイスファイルを自動生成してくれた


## ネットワーク
### ロボットと通信
- ロボットを扱う時は同時に通信も扱っている
- 用途
    - リモート監視・操作等
    - 環境に梅子んだセンサやアクチュエータの操作
    - ソフトウェアのインストール

### IPアドレスの体系（IPv4）
- 0-255の数字を4つドットでつないで表記
    - 例： 192.168.0.1
    - つまり2進数で8桁のものが4つ

- ローカルのものとグローバルのものが存在
    - グローバルIPアドレス（例：8.8.8.8）
        - 世界中でその計算機しか持っていない
    - プライベートIPアドレス（例：192.168.1.1）
        - 閉じた環境で使うアドレス
        - 範囲が決まっている

### ネットワーク部・ホスト部
- IPアドレスを2神数で書いた時、
    - 左側の何桁かは「ネットワーク部」
        - アーネットの中の一つのグループ
    - 残りは「ホスト部」
        - 開くPC固有の番号（住所で言うと番地）
- サブネットマスク
    - どの部分がネットワーク部を表すかを示す数字
        - 例：255.255.255.0（左から24ビットがネットワーク部）
        - 上の例だと、同じルーターに300台とかつなぐとIPアドレス足りない
        - 192.168.0.1/24 とかだと、24ビットがネットワーク部

### コマンド
- ip a
    - 127.0.0.1 は自分自身。
        - これしかないときは、ネットワーク系の機器が全くないことを示す

- arp
    - 次のようにしてラズパイのIPアドレスがわかる
    - arp -a | grep dc:a6

### ルーティング
- 別のネットワーク部にある計算機には無条件でアクセスできない
    - 別のネットワークにパケットを出す設定が必要
    - routel
        - default        192.168.3.1
            - ローカルにないものは、このデフォルトのゲートウェイになげて外にとばせって意味（つまり、ルーター）
            - おれがないとネットワークに届かない

```
traceroute 8.8.8.8
routel
ip r
sudo ip r del default
ip r
sudo ip r add defalt via 192.168... 
```
nmapは外に向けてやると攻撃と思われるので、使い方には注意する
```
nmap -sP 192.168.3.0/24
```

### DHCP
Dynamic Host Configuration Protocol
- ローカルネットワーク上にサーバ（大抵はルータがその役をしている）がいてIPアドレスなどを勝手に設定してくれる
- 通常はこのままDHCPでよい

### ネットワークの設定（手動）
- cd /etc/netplan/ のなかにyamlファイルがある


### ポート
- 計算機が役所のようなものだとすればポートは窓口
    - 窓口は65536*2個ある
        - TCPとUDP

- インターネット上のサービスを利用しているとき
    - 例
        - ラズパイにssh接続：ラズパイのIPアドレスとTCP22番ポート
        - ブラウザに接続。。。443ポート
    - ポートの後ろにサービスを提供する人（サーバー）がいる

### /etc/services
- よく使われるポート番号を表にしたもの
    - ssh: 22
    - http: 80
    - https: 443



## ソフトウェアライセンスとクリエイティブコモンズ

### リチャード・ストールマン
- コードは公開されるべきという立場を作った人
    - ソフトウェアの公開や配布に関するルールに多大な影響

- Emacs, GCC等の作者
    - 1971〜MITのハッカー
    - 様々な逸話

### ハッカー
- 悪いことをする人ではない
    - 悪さをする連中はクラッカーと呼ばれる

- 現代のハッカーは半裸でバンダナではなくパーカーが一般的
- 技術を独占するよりも広く共有して、みんなで大いに楽しみたいとする奔放さ

### ハッカーの自衛
- 今も「ハッカー気質」の人は多い
    - 自分で作ったものは自由に使ってくれという立場だが...
    - こういう考えは他人に利用されやすい→自衛しないといけない

### コピーレフト
- ストールマンが広めた概念
- 著作物は利用・再配布・改編できなければならない
    - つまりフリーダムであるべき
    - Copyleft: all rights reversed
- ただし、著作権は放棄しない
    - 放棄すると防衛が難しくなる

どうするか？

### GPU (GNU General Public License)
- コピーレフトの考え方をライセンス化したもの
- ライセンスとは？
    - プログラムの作成者が利用者に使用させる際につける条件
    - 著作権ではない
- LinuxはGPU

[Linusさん中指](https://www.youtube.com/watch?v=iYWzMvlj2RQ)

### BSD/BSDライセンス
- コードの公開義務なし

### フリーソフトウェア、オープンソフトウェア
- フリーソフトウェア
    - FSFの主張に沿った文脈で使う用語
        - コピーレフトやGPL周辺
- オープンソースソフトウェア
    - open source initiativeという団体の主張に沿った文脈で使う用語
    - ビジネス寄り





## ToDo


## わからないこと
