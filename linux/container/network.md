## コンテナ？

- **隔離**した空間で**プロセス**を実行すること
- cf: VM
  - ホストからは VM のプロセスが見えているだけで、VM 内のプロセスは見えない！
- コンテナはあくまでもホストの上で動くプロセス！
  - うまあく隔離ができているだけ
- コンテナを作る上での主要機能！
  - Namespace
    - 隔離空間を作成
    - コンテナ、そのものかもしれない
  - cgroup
    - CPU・メモリーの制限など

## ファイルシステム

- コンテナ内から、ホスト上のファイルシステムを見えないようにする技術
  - chroot
    - プロセスのルートディレクトリを変更する
    - セキュリティ的に微妙で、docker とかでは使われてない
  - pivot_root
    - chroot のような 抜ける という概念がない
    - バインドマウント `mount --bind dir1 dir2`

## Namespace

- 独立させたいリソースによって幾つかの機能がある！

### いくつかのコマンド

- unshare
  - util-linux
- ip netns
  - iproute2
- ls -l /proc/self/ns
  - 既存の他の Namespace でプロセスを実行したり → setns システムコール
    - docker exec


``` sh
# リンク先の数字（4026531905 など）が Namespace を表す。
$ ls -l /proc/self/ns
total 0
lrwxrwxrwx 1 ubuntu ubuntu 0 May 12 16:14 cgroup -> 'cgroup:[4026531835]'
lrwxrwxrwx 1 ubuntu ubuntu 0 May 12 16:14 ipc -> 'ipc:[4026531839]'
lrwxrwxrwx 1 ubuntu ubuntu 0 May 12 16:14 mnt -> 'mnt:[4026531840]'
lrwxrwxrwx 1 ubuntu ubuntu 0 May 12 16:14 net -> 'net:[4026531905]'
lrwxrwxrwx 1 ubuntu ubuntu 0 May 12 16:14 pid -> 'pid:[4026531836]'
lrwxrwxrwx 1 ubuntu ubuntu 0 May 12 16:14 pid_for_children -> 'pid:[4026531836]'
lrwxrwxrwx 1 ubuntu ubuntu 0 May 12 16:14 user -> 'user:[4026531837]'
lrwxrwxrwx 1 ubuntu ubuntu 0 May 12 16:14 uts -> 'uts:[4026531838]';
```


## Mount Namespace

- Namespace 内のプロセスから見えるマウントポイントの一覧を分離する

``` sh
$ sudo unshare --mount /bin/bash

root@ubuntu:/home/ubuntu# touch /root/hosts
root@ubuntu:/home/ubuntu# mount --bind /etc/host
host.conf    hostname     hosts        hosts.allow  hosts.deny   
# /etc/hosts をバインドマウント
root@ubuntu:/home/ubuntu# mount --bind /etc/hosts /root/hosts 

root@ubuntu:/home/ubuntu# ls -l /root/hosts 
-rw-r--r-- 1 root root 267 Jun 22  2022 /root/hosts

# バインドの情報！
root@ubuntu:/home/ubuntu# grep hosts /proc/self/mountinfo 
2100 1855 179:2 /etc/hosts /root/hosts rw,relatime - ext4 /dev/mmcblk0p2 rw
```

他のシェルから確認 → 空ファイル  
つまり、unshare コマンドで作成した Mount Namespace 内だけでマウントは有効！

``` sh
ubuntu@ubuntu:~$ sudo ls /root/hosts -l
-rw-r--r-- 1 root root 0 May 12 16:20 /root/hosts

# バインドマウントされていない！
ubuntu@ubuntu:~$ grep hosts /proc/self/mountinfo 
```


### pivot_root

pivot_root で新しくルートにするところはマウントポイントでなければならない。

通常のディレクトリーに対して pivot_root するにはバインドマウントが使える。

``` sh
sudo unshare --mount --fork -- /bin/bash

mkdir -p /home/ubuntu/newroot
mount --bind /home/ubuntu/Desktop/ /home/ubuntu/newroot/


# -------- pivot_root 実行 ------------
root@ubuntu:/home/ubuntu/newroot# mkdir old
root@ubuntu:/home/ubuntu/newroot# pivot_root . old


# うーん、pivot_root の先に何も用意してなかったからか？
ls /
bash: /usr/bin/ls: No such file or directory

root@ubuntu:/home/ubuntu/newroot# which ls
which: command not found
root@ubuntu:/home/ubuntu/newroot# type
root@ubuntu:/home/ubuntu/newroot# type ls
ls is aliased to `ls --color=auto'
root@ubuntu:/home/ubuntu/newroot# type -a ls
ls is aliased to `ls --color=auto'
```


### マウントプロぱゲーション

- ある外部ストレージのデータを、システム上の全コンテナから見せたい！というケース
- マウントプロぱゲーション
  - 2つのマウントがあった時に、マウントをお互いに反映させるかさせないかの設定
- 関係しそうな箇所
  - バインドマウント
    - 同じディレクトリーツリーが複数の箇所で見えるようになる
  - Mount Namespace

...


### mountinfo file

``` sh
# カレントプロセス情報へのリンク
$ ls -l /proc/self
lrwxrwxrwx 1 root root 0 Jan  1  1970 /proc/self -> 3233058
```



## UTS Namespace

- Namespace ごとにホスト名やドメイン名を独自に持てる！
- 2006
- sethostname, setdomainname などのシステムコール

``` sh
$ hostname
ubuntu

# UTS Namespace を指定して unshare 実行
sudo unshare --uts /bin/bash

root@ubuntu:/home/ubuntu# hostname
ubuntu
root@ubuntu:/home/ubuntu# hostname pien.example.jp
root@ubuntu:/home/ubuntu# hostname
pien.example.jp
```


## IPC Namespace

- InterProcess Communication で、プロセス間で行われるデータのやり取りのこと
- プロセス間通信（IPC）オブジェクトを Namespace ごとに独立しえt持つことができる
- 独立して持てるオブジェクト
  - System V IPC オブジェクト
  - POSIX メッセージキュー


``` sh
ubuntu@ubuntu:~$ ipcs

------ Message Queues --------
key        msqid      owner      perms      used-bytes   messages    

------ Shared Memory Segments --------
key        shmid      owner      perms      bytes      nattch     status      
0x0052e2c1 0          postgres   600        56         8                       

------ Semaphore Arrays --------
key        semid      owner      perms      nsems     

ubuntu@ubuntu:~$ ipcmk --semaphore 1
Semaphore id: 0
ubuntu@ubuntu:~$ ipcs --semaphore

------ Semaphore Arrays --------
key        semid      owner      perms      nsems     
0x7c1ce8e9 0          ubuntu     644        1 
```


IPC Namespace の作成

``` sh
ubuntu@ubuntu:~$ sudo unshare --ipc

# ホストで作成したものが一切ない、初期化された状態で作られる
root@ubuntu:/home/ubuntu# ipcs

------ Message Queues --------
key        msqid      owner      perms      used-bytes   messages    

------ Shared Memory Segments --------
key        shmid      owner      perms      bytes      nattch     status      

------ Semaphore Arrays --------
key        semid      owner      perms      nsems 
```


## PID Namespace

- Process ID を Namespace ごとに持てる！


## Network Namespace

- ネットワークリソースを Namespace ごとに独立して持つことができる
- 分離されるリソース
  - ネットワークデバイス
  - IPv4, IPv6 プロトコルスタック
  - ルーティングテーブル
  - `/proc/net`
  - `/sys/class/net`
  - ポート番号
  - UNIX ドメインソケットの抽象 Namespace


``` sh
ubuntu@ubuntu:~$ sudo unshare --net /bin/bash

root@ubuntu:/home/ubuntu# ip link show
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00

root@ubuntu:/home/ubuntu# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
```


## User Namespace

- Namespace 機能の中では比較的最近（2013）
- UID, GID の空間を、Namespace ごとに独立してもてる
- **コンテナ内の root ユーザーを、ホスト内では一般ユーザーとして扱うことができる！**
- ホストとコンテナ内で対応付をさせたりする
  - マッピング
- 一般ユーザーでも実行可能！
  - 他と違う
  - なんでだっけ

``` sh
# "0" から始めると root ユーザーから使い始められるよ
# (Namespace 内の最初の ID) (Namespace 外の最初の ID) (範囲)
ubuntu@ubuntu:~$ cat /proc/1/uid_map 
         0          0 4294967295
ubuntu@ubuntu:~$ cat /proc/1/gid_map 
         0          0 4294967295
```

``` sh
# 現在のユーザーの確認
$ whoami; id -u; id -g
ubuntu
1000
1000

# マッピングがされない状態でのマッピング先の確認
$ cat /proc/sys/kernel/overflowuid /proc/sys/kernel/overflowgid 
65534
65534

# unshare 使っちゃう
ubuntu@ubuntu:~$ unshare --user
nobody@ubuntu:~$ echo $$
3248711
nobody@ubuntu:~$ grep "[U|G]id" /proc/3248711/status
Uid:    65534   65534   65534   65534
Gid:    65534   65534   65534   65534
nobody@ubuntu:~$ ls -ld /proc/3248711/status
-r--r--r-- 1 nobody nogroup 0 May 12 17:18 /proc/3248711/status
nobody@ubuntu:~$ id
uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)

# 別のターミナルから、ホスト OS 上の親の Namespace 上でどうなってるか確認！
# つまり、
# ホスト OS の ns での 1000/1000
# → 作成した ns 内の 65534/65534
ubuntu@ubuntu:~$ grep "[U|G]id" /proc/3248711/status
Uid:    1000    1000    1000    1000
Gid:    1000    1000    1000    1000

# マッピングを新規作成！
# 作成した ns の親の ns から実行！　
$ echo '0 1000 1' > /proc/3248711/uid_map
$ echo '0 1000 1' | sudo tee /proc/3248711/gid_map
0 1000 1
# ホスト側からの値は変化してない
ubuntu@ubuntu:~$ grep "[U|G]id" /proc/3248711/status
Uid:    1000    1000    1000    1000
Gid:    1000    1000    1000    1000
# 作成した ns のシェルからは変換ができてる！
nobody@ubuntu:~$ grep "[U|G]id" /proc/3248711/status
Uid:    0       0       0       0
Gid:    0       0       0       0
nobody@ubuntu:~$ id
uid=0(root) gid=0(root) groups=0(root),65534(nogroup)
nobody@ubuntu:~$ ls -ld /proc/3248711
dr-xr-xr-x 9 root root 0 May 12 17:18 /proc/3248711

# --------- ファイル作成など --------
nobody@ubuntu:~$ touch testfile
nobody@ubuntu:~$ ls -l testfile 
-rw-rw-r-- 1 root root 0 May 12 17:31 testfile
# 親の ns からは通常のユーザー
ubuntu@ubuntu:~$ ls -l /home/ubuntu/testfile 
-rw-rw-r-- 1 ubuntu ubuntu 0 May 12 17:31 /home/ubuntu/testfile
```


## コンテナネットワーク

- Network Namespace とコンテナのネットワークは密接に関係している
- コンテナでネットワークを使用する場合、nns を作成
  - コンテナからだけ見えるネットワークインタフェースとなる
- システムコンテナを使う場合、最近は systemd といったソケットを使用する init が使われることが多い
  - → nns をホストとわけ会得のが普通
  - アプリケーションコンテナの場合は init を使わないので、ホストと同じ nns を使うこともあり！


### veth

- 仮想的なネットワークインタフェース
- レイヤー2の仮想ネットワークインタフェース
- 対となる2つのインタフェースが作成され
  - その間で通信がおこなえる
  - → **レイヤー2のトンネリング！**
- veth を使う時は、ホスト上にブリッジを作る！
  - ブリッジ上で NAT することも、ホストと同じネットワークに属することも可能
- コンテナ用といってもいいくらいの機能

``` sh
# veth ペアの作成
ubuntu@ubuntu:~$ sudo ip link add name veth0-host type veth peer name veth0-ct

ubuntu@ubuntu:~$ sudo ip link show
41: veth0-ct@veth0-host: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 76:85:ef:07:df:f8 brd ff:ff:ff:ff:ff:ff
42: veth0-host@veth0-ct: <BROADCAST,MULTICAST,M-DOWN> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether be:65:06:58:63:b9 brd ff:ff:ff:ff:ff:ff

# veth0-host にアドレスを設定
sudo ip addr add 10.10.10.10/24 dev veth0-host
sudo ip addr add 10.10.10.11/24 dev veth0-ct
# up
sudo ip link set up veth0-host
sudo ip link set up veth0-ct

ubuntu@ubuntu:~$ sudo ip link show
41: veth0-ct@veth0-host: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 76:85:ef:07:df:f8 brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.11/24 scope global veth0-ct
       valid_lft forever preferred_lft forever
    inet6 fe80::7485:efff:fe07:dff8/64 scope link 
       valid_lft forever preferred_lft forever
42: veth0-host@veth0-ct: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether be:65:06:58:63:b9 brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.10/24 scope global veth0-host
       valid_lft forever preferred_lft forever
    inet6 fe80::bc65:6ff:fe58:63b9/64 scope link 
       valid_lft forever preferred_lft forever

ubuntu@ubuntu:~$ ping -I veth0-host 10.10.10.11


ubuntu@ubuntu:~$ sudo ip netns add netns01
ubuntu@ubuntu:~$ sudo ip netns list
netns01
# veth0-ct を netns01 に移動させる
ubuntu@ubuntu:~$ sudo ip link set veth0-ct netns netns01

# netns01 の ns 内でコマンドを実行する
ubuntu@ubuntu:~$ sudo ip netns exec netns01 ip link show
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
41: veth0-ct@if42: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/ether 76:85:ef:07:df:f8 brd ff:ff:ff:ff:ff:ff link-netnsid 0

# veth0-ct に IP を割り当てて有効にする！
ubuntu@ubuntu:~$ sudo ip netns exec netns01 ip addr add 10.10.10.11/24 dev veth0-ct
ubuntu@ubuntu:~$ sudo ip netns exec netns01 ip link set veth0-ct up
ubuntu@ubuntu:~$ sudo ip netns exec netns01 ip addr show
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
41: veth0-ct@if42: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 76:85:ef:07:df:f8 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.10.10.11/24 scope global veth0-ct
       valid_lft forever preferred_lft forever
    inet6 fe80::7485:efff:fe07:dff8/64 scope link 
       valid_lft forever preferred_lft forever

# ping が通るようになったぞぉ〜〜〜〜
# veth は、ペアが互いに異なる nns に存在しなければ通信ができない！
ubuntu@ubuntu:~$ ping -I veth0-host 10.10.10.11
PING 10.10.10.11 (10.10.10.11) from 10.10.10.10 veth0-host: 56(84) bytes of data.
64 bytes from 10.10.10.11: icmp_seq=1 ttl=64 time=0.258 ms
64 bytes from 10.10.10.11: icmp_seq=2 ttl=64 time=0.140 ms
64 bytes from 10.10.10.11: icmp_seq=3 ttl=64 time=0.153 ms
```


### macvlan

- ホストと同じネットワークにコンテナを接続する場合
  - macvlan というインタフェースが使える
- １つのインタフェースに複数の MAC アドレスを割り当てられる機能
  - MAC アドレスを持つので、DHCP でアドレスを割り当てることが可能
    - IP エイリアスとの違い
- モード
  - private
  - bridge
  - vepa
  - passthru



