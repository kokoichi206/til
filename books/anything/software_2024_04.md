## なんでも

- CheerpJ
  - Web ブラウザで Java プログラムを実行できる
- 権威サーバ
  - 責任重大だ
  - ルートサーバへのアクセスができないことは、事実上インターネットが利用できないことと同義
  - TTL の時間だけ、障害が自動的に継続されてしまう。。。
    - DNS の操作の時は一旦 TTL を 60 秒ほどにし
    - 操作完了後 3600 s ほどに伸ばしておく
  - **ネガティブキャッシュ**
    - サブドメインの設定追加前に、誰かがそのサブドメインにアクセスしてしまった時など。。。
    - 別のキャッシュサーバを利用、非再起問い合わせをする、など
- GCP
  - BigQuery
    - DWH
    - 数 TB くらいの処理だったら数十秒程度で完了する
    - フルマネージド
  - データパイプライン
    - あるデータソースから BigQuery までデータを届けるシステム
    - ここでは ELT を採用する
  - ELT:
    - Extract 抽出
    - Load 書き込み、事前処理
    - Transform 変換
- NewsPicks
  - Bitrise
    - Firebase Test Lab
    - UI テスト
  - TCA アーキテクチャ
    - The Composable Architecture
    - SwiftUI との親和性が高い
  - VRT:
    - Visual Regression Testing
    - [iOSアプリ開発でVisual Regression Testingを導入しUIのデグレ検知を自動化した話](https://tech.uzabase.com/entry/2023/06/05/122838)
- キャッシュ
  - サービスが強くキャッシュに依存し、壊れやすくなることがある。。。
  - **キャッシュは麻薬**
    - 過度な忌避もダメ
  - **極めるべきこと**
    - 対象データ
    - 適切なキャッシュアルゴリズム
    - 存在期間
  - まずは RDBMS の能力を使い切ることを考える！
  - **キャッシュと相性が良いデータ**
    - 頻繁にアクセスされる
    - コストの高い計算処理
    - 更新頻度が低い
  - [「キャッシュは麻薬」という標語からの脱却](https://onk.hatenablog.jp/entry/2023/12/18/000000)
    - 2種類区別
      - アプリケーションレイヤでのキャッシュ
      - HTTP レイヤでのキャッシュ
    - キャッシュを再構築できない場合は使うべきではない！
- 位置情報
  - クライアントサイドでの空間演算
    - https://turfjs.org/
- AWS
  - オペレーションの自動化
  - Systems Manager
- `killall yes`
  - `man killall`

## Linux

### file system

- パーティションの管理
  - MBR, GPT
    - MBR は古い
- PC の起動
  - BIOS
    - 古い
  - UEFI
    - 新しい
    - GPT のパーティションのみ！
- パーティション

``` sh
man parted

$ lsblk | grep -v '^loop[0-9]'
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
mmcblk0     179:0    0  59.5G  0 disk 
├─mmcblk0p1 179:1    0   256M  0 part /boot/firmware
└─mmcblk0p2 179:2    0  59.2G  0 part /


$ man lsblk
LSBLK(8)                                                 System Administration                                                LSBLK(8)

NAME
       lsblk - list block devices
```

- ファイルシステム
  - ファイルという抽象的なアクセス手段を提供する仕組み
  - NTFS: Windows
  - ext4/xfs/btrfs: Linux
  - FAT32/exFAT: USB, SD

``` sh
# ファイルシステムも出力してくれる
$ df -T
Filesystem     Type     1K-blocks     Used Available Use% Mounted on
udev           devtmpfs   3947580        0   3947580   0% /dev
tmpfs          tmpfs       799876     6368    793508   1% /run
/dev/mmcblk0p2 ext4      61094344 56059396   2509032  96% /
tmpfs          tmpfs      3999372       28   3999344   1% /dev/shm

# mount とかでもいい
```

- LVM: Logical Volume Manager
  - ボリュームを抽象化して扱う Linux の機能
  - ディスク上のパーティションを直接使用するのではない
  - Ubuntu Server ではデフォルトで使われる
  - スナップショット機能がある
    - Copy on Write

``` sh
lvscan
```

- RAID
  - Redundant Arrays of Inexpensive Disks
- Linux MD
  - ソフトウェア RAID
- ファイル
  - Linux はシステム全体で単一のディレクトリツリー
  - FHS:
    - Filesystem Hierarchy Standard
      - https://ja.wikipedia.org/wiki/Filesystem_Hierarchy_Standard
    - ディレクトリツリーの標準仕様
    - FHS3.0
      - https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.pdf
- **UsrMerge**
  - わかりにくいよね！ってやつ
  - 全てのコマンドを `/bin` でも `/usr/bin` でも呼び出そっての
  - Ubuntu ではデフォルトで採用
  - **ファイルシステムとしては**マージされている
    - **パッケージシステムは依然として使い分けている**

``` sh
# UsrMerge
$ ls -l /{bin,sbin,lib*}
lrwxrwxrwx 1 root root 7 Feb  1  2021 /bin -> usr/bin
lrwxrwxrwx 1 root root 7 Feb  1  2021 /lib -> usr/lib
lrwxrwxrwx 1 root root 8 Feb  1  2021 /sbin -> usr/sbin
```

- ファイルシステム上のデータ
  - データの内容
  - メタ情報: inode
    - ファイルの種類
    - オーナー
    - パーミッション
- ハードリンク
  - 効率的なバックアップ
  - inode 番号を参照するため、**異なるファイルシステムを跨いだリンクは作成できない**
- シンボリックリンク
  - **パス名**を指定してリンク
  - **リンク先のファイル名を変更するとリンクが切れてしまう！**

``` sh
# ハードリンク
ln file1 hardfile1

$ ls -i -1
1272771 file1
1272771 hardfile1

# ハードリンク
ln -s file1 symfile1

$ ls -il -1
1272771 -rw-rw-r-- 2 ubuntu ubuntu    0 Aug  8  2021 file1
1272771 -rw-rw-r-- 2 ubuntu ubuntu    0 Aug  8  2021 hardfile1
1269762 lrwxrwxrwx 1 ubuntu ubuntu    5 Mar 20 06:09 symfile1 -> file1
```

### プロセス

- プロセスの状態
  - 実行可能
    - まさに CPU を使っている・使いたい
  - 中断可能なスリープ
  - 中断不可能なスリープ
    - デバイスへの I/O まち
    - プロセスを強制終了することもできない

``` sh
# S(state) が R(running)
$ yes >/dev/null & pid=$!; sleep 1; ps -q $pid -o pid,s,cmd; kill $pid
[1] 3058342
    PID S CMD
3058342 R yes
[1]+  Terminated              yes > /dev/null

# S(state) が S(sleeping = 中断可能なスリープ)
$ sleep 10 & pid=$!; sleep 1; ps -q $pid -o pid,s,cmd; kill $pid
[1] 3059272
    PID S CMD
3059272 S sleep 10
[1]+  Terminated              sleep 10



$ sleep 100 &
[1] 3062184
$ ps -O ppid
    PID    PPID S TTY          TIME COMMAND
3062184 3828606 S pts/4    00:00:00 sleep 100
3062205 3828606 R pts/4    00:00:00 ps -O ppid


# init プロセスは systemd!
$ pstree -p | head
systemd(1)-+-agent(1963)-+-{agent}(2322)
           |             |-{agent}(2324)
           |             |-{agent}(2330)
           |             |-{agent}(2331)
```

- pstree
  - init プロセスより始まる
- 終了
  - プロセスが終了すると、親プロセスに通知される！


``` sh
$ PS1='(2nd) $ '
(2nd) $ yes >/dev/null &
[1] 3064908
(2nd) $ ps -O ppid
    PID    PPID S TTY          TIME COMMAND
3064415 3828606 S pts/4    00:00:00 bash
3064908 3064415 R pts/4    00:00:02 yes
3065003 3064415 R pts/4    00:00:00 ps -O ppid
3828606  992070 S pts/4    00:00:02 /bin/bash --init-file /home/ubuntu/.vscode-server/bin/903b1e9d8990623e3d7da1df3d33db3e42d80eda/out/vs/
(2nd) $ kill -9 $$
Killed

# 親プロセスが死ぬ → init が親プロセスになる！（yes）
$ ps -O ppid
    PID    PPID S TTY          TIME COMMAND
3064908       1 R pts/4    00:00:38 yes
3065417 3828606 R pts/4    00:00:00 ps -O ppid
3828606  992070 S pts/4    00:00:02 /bin/bash --init-file /home/ubuntu/.vscode-server/bin/903b1e9d8990623e3d7da1df3d33db3e42d80eda/out/vs/
```

- スレッド
  - プロセスの中にあるもの
  - 同じプロセスの中でメモリ空間を共有
  - CPU 上で実行中のアドレスなど実行の状態が異なる
- カーネルスレッド
  - カーネルの中で動くスレッド
  - ps コマンドの出力の中で `[]` がついているもの！

``` sh
$ ps ax | head
    PID TTY      STAT   TIME COMMAND
      1 ?        Ss   2547:32 /sbin/init fixrtc splash
      2 ?        S      0:28 [kthreadd]
      3 ?        I<     0:00 [rcu_gp]
      4 ?        I<     0:00 [rcu_par_gp]


$ ln -s /bin/yes '[foo]'
# PATH の先頭に PWD を持ってくることにより、
# シェルがコマンドを探すときに現在のディレクトリが最優先で検索されるようになる！
$ PATH=$PWD:$PATH \[foo\] >/dev/null &
[1] 3070082
$ ps
    PID TTY          TIME CMD
3070082 pts/4    00:00:01 [foo]
3070185 pts/4    00:00:00 ps
3828606 pts/4    00:00:02 bash


# 通常のカーネルスレッドの場合, exe がリンクされてない！
$ ls -l /proc/3070082/exe
lrwxrwxrwx 1 ubuntu ubuntu 0 Mar 20 06:36 /proc/3070082/exe -> /usr/bin/yes


$ kill 3070082
[1]+  Terminated              PATH=$PWD:$PATH \[foo\] > /dev/null
$ rm ./'[foo]'


# https://github.com/dalance/procs
procs -i Docker
procs -w --sortd cpu


$ pgrep -a yes
3080397 yes
$ kill -KILL 3080397
```

- top
  - bashtop, htop なども出てるよ
- kill
  - SIGHUP
    - サーバの設定を再読み込みさせるためなんかにも使われる
- 優先度
  - -20 ~ 19 で指定
  - **マイナスの方が優先される**
- スケジューリングポリシー
  - NORMAL
  - BATCH
    - プロセスの切り替わりが起こりにくくなる
    - 1 回の CPU 時間が長くなり、キャッシュの活用が進む
  - IDLE
- ulimit
  - hard limit
    - ハードウェアの制限
    - `ulimit -aH`
  - soft limit
    - ユーザー自身がここまで引き上げられるやつ
    - `ulimit -a`
  - プロセスやユーザー単位での制限
- CGroups
  - Control Groups
  - プロセスのグループを作る

``` sh
$ cd /sys/fs/cgroup/
$ ls -F
blkio/  cpuacct@      cpuset/   freezer/  net_cls,net_prio/  perf_event/  rdma/     unified/
cpu@    cpu,cpuacct/  devices/  net_cls@  net_prio@          pids/        systemd/
```

### ユーザー管理

- su command
  - `-`, `--login`
    - ログインシェルで起動

``` sh
sudo tail -f /var/log/messages

# root のパスワード変更。
sudo passwd
```

- sudo 設定ファイル
  - `/etc/sudoers`
    - **影響力がより強い**
    - `visudo` コマンドがある！！
  - `/etc/sudo.conf`

``` sh
sudo sh -c "grep root /etc/shadow > root-user-dire/sample"
sudo grep root /etc/shadow | sudo tee root-user-dire/sample
```

- runuser
  - `sudo u <user_name> command` 的なことができる
  - **password, tty が不要！！！**
  - スクリプト内で便利だったり！

``` sh
cat /etc/group

cat /etc/passwd
```

- chmod
- chown
- umask
  - ファイルなら666, ディレクトリなら777から **umask 値を引いた値が設定される！**
  - **umask　はログイン時に設定されている！**
  - シェルの内部コマンド

``` sh
$ umask
0002


$ cat ~/.profile | grep umask
# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022
```

- setuid, setgid
  - これがついてる実行ファイルは、**一般ユーザーにかわりファイル所有者の権限で**実行される

``` sh
# rws になってるの！
$ ls -l /bin/passwd 
-rwsr-xr-x 1 root root 63744 May 28  2020 /bin/passwd


# sudo 履歴の監視。
journalctl /usr/bin/sudo | head -n 5

$ journalctl /usr/bin/su
-- Logs begin at Sat 2024-03-16 14:39:43 UTC, end at Wed 2024-03-20 07:49:27 UTC. --
-- No entries --
```

### ネットワーク

- ping
  - ICMP プロトコルを使用


``` sh
$ ip addr show

# ルーティングの設定を確認。
ip route

# ポートの状態を確認する！！
# -l: 待ち受け状態のポート, -t: TCP, -n: number, -4: IPv4, -p: process
$ ss -ltn4p

sudo ufw status verbose
```


## テクニカルライティング

- 特徴
  - 説明対象が存在している
  - 誤解を生まない
  - 明確で理解しやすい
  - 読み手に行動を促す
  - 文章が成果物
- 読み手に合わせる
  - 前提知識を考える
  - 対象を絞り込むことも大事
    - どのくらいの知識量を持つ読み手を対象としてるか
    - このドキュメントで説明すること
    - 説明しないこと
  - 理解の効率とメンタルモデル
- アウトラインの作成
  - アウトライン**から**作成する
  - 伝えるべき情報を階層構造に！
  - 順序の決め方
    - 重要度
    - ニーズの大きさ
    - 既知から未知に
    - 時系列
- ドキュメントは一部しか読まれない
  - 短時間で知りたい情報に辿り着きたい
  - 重要なことから
  - できるだけ短く
  - 一文一義！
- 読み手の視点でかく
  - 『主語が動作を行う』形式の文章の方がいい

## Chrome

- Blink
  - レンダリングエンジン
  - 機能
    - HTML/CSS の解析・レンダリング
    - JavaScript を通した API の提供
  - content public API
- プロセス
  - ブラウザプロセス
    - 制御
    - 1つしか存在しない
  - レンダープロセス
    - Blink の実行されてるプロセス
    - サイトごとに作られる
  - Viz プロセス
    - GPU を利用してブラウザの UI や Web ページを組み合わせる
    - 1つしかない
- RenderingNG
  - https://developer.chrome.com/docs/chromium/renderingng?hl=ja
- V8
  - Google が開発してる OSS エンジン
  - https://github.com/v8/v8
