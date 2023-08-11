## expect

```
$ uname -a
Linux ubuntu 5.4.0-1045-raspi #49-Ubuntu SMP PREEMPT Wed Sep 29 17:49:16 UTC 2021 aarch64 aarch64 aarch64 GNU/Linux

$ expect -version
expect version 5.45.4
```

``` sh
systemctl restart sakamichi-api-bff.service
==== AUTHENTICATING FOR org.freedesktop.systemd1.manage-units ===
Authentication is required to restart 'sakamichi-api-bff.service'.
Authenticating as: Ubuntu (ubuntu)
Password:
```

``` sh
$ cat zero.sh 
#!/bin/bash

systemctl restart sakamichi-api-bff.service
```

``` sh
$ cat expect.sh

#!/bin/bash

expect -c "
    # 5 秒でタイムアウトにする。
    set timeout 5
    # 実行したいコマンド。
    spawn systemctl restart sakamichi-api-bff.service

    # ターミナル上に現れることが期待される文言。
    expect \"Password:\"
    # 打ち込みたい内容。パスワードの例。
    send \"root_pass\"
    send \"\n\"

    expect \"$:\"
    exit 0
"
```

## data 収集

```sh
strace -o trace-zero bash zero.sh
strace -f -o trace-zero-with-f bash zero.sh

strace -f trace-expect bash expect.sh
strace -f -o trace-expect-with-f bash expect.sh

cat trace-expect-with-f 
```

出力が多すぎるので、何とか工夫して比較していきたいです。
（`-f` つけなかった時は 270 行くらい）

``` sh
$ cat trace-expect-with-f | wc -l
4776
```

## 比較

``` sh
# ぱっと見、重要な違いはなさそうう？？
diff <(cat trace-expect | sed 's@(.*@@g') <(cat trace-zero | sed 's@(.*@@g') > diff_without_f.diff

# 数が多すぎてわからない！！
diff <(cat trace-expect-with-f | sed 's@(.*@@g' | awk '{print $2}' ) <(cat trace-zero-with-f | sed 's@(.*@@g') > diff_with_f.diff
```

### コマンドレベルでの違い

expect の有無で、呼ばれるシステムコールのコマンドにどんな違いがあるか見てみます。
（-f オプション付きの時）

```sh
$ cat trace-expect-with-f | sed 's@(.*@@g' | awk '{print $2}' | grep '[a-z]' | sort | uniq -c | sort -nr
    393 mmap
    373 openat
    354 rt_sigaction
    290 newfstatat
    228 mprotect
    215 close
    212 munmap
    201 futex
    191 read
     90 write
     88 ppoll
     55 ioctl
     48 faccessat
     47 fcntl
     45 rt_sigprocmask
     33 recvmsg
     30 execve
     30 brk
     18 set_robust_list
     18 geteuid
     15 sendmsg
     15 pselect6
     15 prlimit64
     13 lseek
     13 getpid
     12 rseq
     12 readlinkat
     12 prctl
     12 getuid
     12 getegid
     11 clone
     10 getrandom
     10 getgid
      8 statfs
      8 set_tid_address
      8 pipe2
      8 getdents64
      7 sched_yield
      7 eventfd2
      6 socket
      6 kill
      6 getsockopt
      6 exit_group
      6 dup3
      6 connect
      5 wait4
      5 getppid
      4 sendto
      4 fstat
      3 rt_sigreturn
      3 recvfrom
      3 gettid
      2 writev
      2 waitid
      2 uname
      2 setsockopt
      2 fdatasync
      1 umask
      1 sysinfo
      1 syscall_0x1b7
      1 signalfd4
      1 setsid
      1 sched_setattr
      1 sched_getattr
      1 restart_syscall
      1 mknodat
      1 mkdirat
      1 madvise
      1 inotify_init1
      1 inotify_add_watch
      1 getsockname
      1 getpgid
      1 exit
      1 clock_nanosleep

$ cat trace-zero-with-f | sed 's@(.*@@g' | awk '{print $2}' | grep '[a-z]' | sort | uniq -c | sort -nr
    345 mmap
    296 openat
    238 newfstatat
    202 mprotect
    189 munmap
    162 close
    156 rt_sigaction
    151 read
    142 futex
     89 ppoll
     65 write
     34 rt_sigprocmask
     33 recvmsg
     27 ioctl
     21 faccessat
     17 brk
     16 geteuid
     15 sendmsg
     13 fcntl
     12 set_robust_list
     12 prlimit64
     12 prctl
     11 getegid
     10 getuid
     10 getpid
      9 getgid
      8 statfs
      8 rseq
      8 getdents64
      7 getrandom
      7 eventfd2
      7 clone
      6 sched_yield
      6 lseek
      6 kill
      6 getsockopt
      5 set_tid_address
      5 execve
      4 socket
      4 sendto
      4 pipe2
      4 getppid
      4 fstat
      4 dup3
      4 connect
      3 wait4
      3 recvfrom
      3 gettid
      3 exit_group
      2 writev
      2 waitid
      2 setsockopt
      2 rt_sigreturn
      2 fdatasync
      1 uname
      1 umask
      1 sysinfo
      1 syscall_0x1b7
      1 signalfd4
      1 sched_setattr
      1 sched_getattr
      1 mknodat
      1 mkdirat
      1 inotify_init1
      1 inotify_add_watch
      1 getsockname
      1 getpgid
      1 clock_nanosleep
```

### expect だけの system call あるか　

```sh
$ diff <(cat trace-expect-with-f | sed 's@(.*@@g' | awk '{print $2}' | grep '[a-z]' | sort | uniq) <(cat trace-zero-with-f | sed 's@(.*@@g' | awk '{print $2}' | grep '[a-z]' | 
sort | uniq)
9d8
< exit
33d31
< madvise
45d42
< pselect6
47d43
< readlinkat
50d45
< restart_syscall
61d55
< setsid
```

chat-gpt に雑に投げてみます。

> expect のコマンドを使うと、strace を通していかの systemcall が確認できたのですが、どんな意味ですか？
> 
> 9d8
> < exit
> 33d31
> < madvise
> 45d42
> < pselect6
> 47d43
> < readlinkat
> 50d45
> < restart_syscall
> 61d55
> < setsid

```
straceを使用すると、プログラムが発行するシステムコールの一覧をキャッチできます。このリストから、expectコマンドが使用しているシステムコールが確認できるようです。それぞれのシステムコールについて、簡単に説明します：

exit: プロセスの終了を行います。このシステムコールが呼び出されると、プロセスはその実行を終了し、リソースを解放します。

madvise: このシステムコールは、メモリの使用に関するアドバイスをカーネルに提供します。例えば、特定のメモリ範囲が将来的にアクセスされないことをカーネルに伝えるために使用されることがあります。

pselect6: selectのように、複数のファイルディスクリプタを監視し、いずれかが読み取り/書き込みのために利用可能になるのを待ちます。さらに、シグナルマスクの指定も可能です。

readlinkat: シンボリックリンクの内容を読み取るためのシステムコールです。これは、リンクの実際のパスを取得するために使用されます。

restart_syscall: このシステムコールは、一時停止したシステムコールの再開を試みる時に使用されます。特定のシグナルを受信してシステムコールが中断された場合にこの動作が発生することがあります。

setsid: 新しいセッションを作成し、呼び出したプロセスを新しいセッションのリーダーにします。これは、通常デーモンプロセスがバックグラウンドで実行される際に使用されます。

これらのシステムコールは、expectが子プロセスを管理し、入力/出力を監視し、その動作に応じて反応するためのものです。
```

気になったものについて、少し調べてみます。

### pselect6 周り

[pselect6](https://manpages.debian.org/testing/manpages-ja-dev/pselect6.2.ja.html) 周りの strace の出力を見てみます。

その前に、pselect6 以外に、select 系のシステムコールが呼ばれてないか確認しておきます。

``` sh
# 他の select 系はなさそう + pselect6 は 15 回呼ばれてそう
$ cat trace-expect-with-f | sed 's@(.*@@g' | awk '{print $2}' | grep '[a-z]' | sort | uniq -c | sort -nr | grep sel
     15 pselect6
```

以下のような unfinished の状態と resumed による監視再開の trace しかなく、特に面白くはなかったですが少しみてみます。

```
138438 pselect6(6, [5], [], [], NULL, NULL <unfinished ...>
...
138438 <... pselect6 resumed>)          = 1 (in [5])
```

全体的に第二引数に `[5]` が指定されており、FD 5 が常に監視されていそうでした。
（第一引数により 0-5 までを対象としており、そのうち 5 のみを監視しています。）

ここの FD5 というのはどこで定義されてるのでしょうか。

```
361333 ioctl(4, TIOCGPTPEER, 0x102)     = 5
```

説明

```
ファイルディスクリプタ4: このioctlコマンドが操作するデバイスやファイルのディスクリプタ。

TIOCGPTPEER: このコマンドは、与えられた(主)側の端末のペアである(従)側の端末を取得するためのものです。具体的には、これは、主端末側で実行すると、従端末側のファイルディスクリプタを返します。このコマンドは、新しいセッションを開始する際などに、従端末の端末属性を取得したり設定したりするために使用されることがあります。

0x102: このフラグは、TIOCGPTPEERの動作に影響を与える追加の情報や指示を提供するために使用される可能性があります。この場合、O_RDWR | O_NOCTTY（数値的には0x102）のフラグが指定されており、これは従端末を読み書きの両方で開くことを意味しています。また、O_NOCTTYは、この端末を呼び出し側の制御端末として設定しないことを指示しています。

このioctl呼び出しの結果、従端末のファイルディスクリプタ5が返されています。
```

また、以下の trace で、`/dev/pts` (ubuntu の擬似 tty) を、シンボリックリンクの内容を読み取ったりしています。

```
361333 newfstatat(5, "", {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0x7), ...}, AT_EMPTY_PATH) = 0
361333 readlinkat(AT_FDCWD, "/proc/self/fd/5", "/dev/pts/7", 4095) = 10
361333 newfstatat(AT_FDCWD, "/dev/pts/7", {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0x7), ...}, 0) = 0
361333 close(5)                         = 0
...
361334 openat(AT_FDCWD, "/dev/pts/7", O_RDWR) = 0
```

ちなみに、実行直前に擬似 tty を調べたら 6 までしかなかったため、新たに作成された 7 番であると推測できます。

``` sh
$ ls /dev/pts
0  1  2  3  4  5  6  ptmx
```

### readlinkat 周り

上でも `readlinkat` は出てきましたが、他にも気になるのが `tcltk` を読んでる部分です。
もろに expect に関係してそうです。

```
138434 readlinkat(AT_FDCWD, "/usr/share/tcltk", 0xfffffa136c50, 1023) = -1 EINVAL (Invalid argument)
```

