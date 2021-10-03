## Linux 環境の調査、設定と活用

### ファイル
- /var
  - 変化するデータのファイル
- boot.log
  - /var/log/boot.log
- `$ sudo cat /etc/hostname`

```sh
$ df -Th | awk '$1 == "Filesystem" || $1 ~ "^[^/]"'
Filesystem     Type      Size  Used Avail Use% Mounted on
udev           devtmpfs  3.8G     0  3.8G   0% /dev
tmpfs          tmpfs     782M  6.2M  776M   1% /run
tmpfs          tmpfs     3.9G   28K  3.9G   1% /dev/shm
tmpfs          tmpfs     5.0M  4.0K  5.0M   1% /run/lock
tmpfs          tmpfs     3.9G     0  3.9G   0% /sys/fs/cgroup
tmpfs          tmpfs     782M   84K  782M   1% /run/user/1000

$ df -Th | awk 'NR == 1 || $NF == "/"'
Filesystem     Type      Size  Used Avail Use% Mounted on
/dev/mmcblk0p2 ext4       59G   22G   35G  39% /
```

mmcblk0 として OS に認識されている記憶デバイスの、2 番目のパーティション

```sh
$ ls -i /
   14 bin       2 dev   1491 home     11 lost+found   1494 mnt    
    1 proc      2 run    1505 snap      1 sys   1528 usr
   15 boot     44 etc   1492 lib    1493 media        1495 opt  
 1497 root   1504 sbin   1525 srv    1527 tmp  71804 var

# ファイル(iノード)に対してファイル名を複数つける機能がある。
# ファイル名から i ノードへの対応をリンクという
$ seq 1 99 | while read i ; do ln hoge $i ; done
$ ls -l hoge
```

ファイル名の最長

```sh
$ yes | ruby -nle 'puts $_ *$.' | while read f && touch $f; do echo ${#f} && rm $f; done | tail -n 1
touch: cannot touch 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy': File name too long
255
Traceback (most recent call last):
        3: from -e:1:in `<main>'
        2: from -e:1:in `puts'
        1: from -e:1:in `puts'
-e:1:in `write': Broken pipe @ io_writev - <STDOUT> (Errno::EPIPE)
```

### No.105 ディスク使用料の集計
```sh
$ paste <(du -sh /usr/*) <(du -s /usr/* | awk '{print $1}') |\
 sort -k3,3nr | awk '{print $1,$2}'
3.7G /usr/lib
1.5G /usr/share
797M /usr/bin
378M /usr/src
216M /usr/include
81M /usr/sbin
12M /usr/libexec
4.2M /usr/local
704K /usr/games

$ du -s /usr/* | sort -nr | awk '{print $2}' | xargs du -sh
# sort -rh の、h = --human-numeric-sort
$ du -sh /usr/* | sort -rhk1,1
```

### No.106
```sh
$ ls -l /bin/ | awk '$1 !~ /^[lxrw-]*$/'
$ ls -l /bin/ | awk '$1 ~ /[^lxrw-]/'
```

s ??

Set User ID or Set Group ID

SUID が付与されたコマンドは、実行したユーザーではなく、所有者の権限で実行できる。

### No.107
何回 root になったか

```sh
$ cat /var/log/auth.log | grep sudo | wc -l | xargs -I@ echo @/3 | bc
15

$ zgrep -a '(sudo:session): session opened for user root' /var/log/auth.log* | sed -r 's/^[^:]+://' | awk '{print $1}' | sort | uniq -c
      1 Aug
      6 Oct
    118 Sep
```

### 中身が同じファイルの検索
md5sum のハッシュ値（MD5値）を使う

```sh
$ sudo find /etc -type f | sudo xargs md5sum
0e0f36cafc6a9cf76bc704cfd8f96ece  /etc/iproute2/ematch_map
18bfdabbd4d5b14eae350720ea5ff431  /etc/iproute2/rt_tables.d/README
7137bdf40e8d58c87ac7e3bba503767f  /etc/iproute2/rt_realms
3aea2c0e0dd75e13a5f8f48f2936915f  /etc/iproute2/group
393e42fa549d0974eb66d576675779c2  /etc/iproute2/nl_protos
a1313318d6778fe6b8c680248ef5a463  /etc/iproute2/rt_tables
7b2dc3e981ec34331766ba9d219670aa  /etc/iproute2/rt_protos
88e45597012c565f9a10ffef1bc14312  /etc/iproute2/rt_protos.d/README
6298b8df09e9bda23ea7da49021ca457  /etc/iproute2/rt_scopes
4c80d267a84d350d89d88774efe48a0f  /etc/iproute2/rt_dsfield
...
```

答え

```sh
$ sudo find /etc -type f | sudo xargs md5sum |\
 awk '{a[$1]=a[$1]" "$2}END{for(k in a){print k, a[k]}}' | awk 'NF > 2'
912170431ea78ea8139735cafa6d9b40  /etc/subuid /etc/subgid
476028824e6fefb251ded3df27a420b3  /etc/network/if-down.d/postfix /etc/ppp/ip-down.d/postfix
1f83c20a8d7e267e792f0a72a19ba563  /etc/letsencrypt/keys/0005_key-certbot.pem /etc/letsencrypt/archive/kokoichi0206.mydns.jp/privkey2.pem
e5e12910bf011222160404d7bdb824f2  /etc/cron.daily/.placeholder /etc/cron.hourly/.placeholder /etc/cron.monthly/.placeholder /etc/cron.weekly/.placeholder /etc/cron.d/.placeholder
d6b276695157bde06a56ba1b2bc53670  /etc/python2.7/sitecustomize.py /etc/python3.8/sitecustomize.py
23931e8dd5833b30686dfc11c898cc39  /etc/postfix/master.cf /etc/postfix/master.cf.proto
706a20e6babc707e9a3d002b2c130af3  /etc/sane.d/dc210.conf /etc/sane.d/dc240.conf
272913026300e7ae9b5e2d51f138e674  /etc/magic /etc/magic.mime
...
```

### 擬似ファイルシステム
```sh
$ df -Ta | awk '$2'
```





## 小ネタ
- grep -a は、バイナリファイル内を検索するのに使える！
  - 行儀の悪いログが多いので、つけるのをお勧め
