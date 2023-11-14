## sec 1

- カーネル
  - 命令の実行順序の正しい制御
    - 最悪文鎮化 (brick)
  - CPU のモード
    - カーネルモードとユーザーモード
- システムコール
  - プロセスがカーネルに処理を依頼するための方法
  - システムに搭載されている論理 CPU が実行している命令の割合 → sar コマンド
  - sar
    - system はシステムコールを処理している時間の割合

``` sh
# -P 0 論理 CPU0 のデータ
# 1 1 秒ごとに
# 1 1 回だけ
sar -P 0 1 1
```

- ライブラリ
  - 標準 C ライブラリ
    - glibc
    - libc
  - プログラムがどのようなライブラリをリンクしているかは ldd コマンドで見れる！

``` sh
ldd /bin/echo

        linux-vdso.so.1 (0x0000ffffba162000)
        libc.so.6 => /lib/aarch64-linux-gnu/libc.so.6 (0x0000ffffb9f50000)
        /lib/ld-linux-aarch64.so.1 (0x0000ffffba129000)
```

- システムコールのラッパー関数
  - libc は標準 C のライブラリでだけではない
  - **システムコールは通常の関数呼び出しと違って C 言語などの高級言語から直接呼び出せない！**
    - **アーキテクチャ依存のアセンブリコードを使って呼び出す**必要がある
- 静的ライブラリか共有ライブラリか
  - サイズと ldd コマンドの実行結果
  - 共有ライブラリが今までは好んで使われてきた
  - 一方 **Go 言語は基本的にライブラリを全て静的リンクにしている！**
    - メモリやストレージの大容量化によってサイズの問題は相対的に小さくなった
    - プログラムが1つの実行ファイルだけで動けば、当該ファイルをコピーするだけで別の環境でも動作するので扱いが楽
    - 実行時に共有ライブラリをリンクしなくて済むので起動が高速
    - 共有ライブラリの DLL 地獄と呼ばれる問題を回避できる

## sec 2

- ps aux
  - ps aux --no-header
- プロセスの生成
  - 同じプログラムの処理を複数のプロセスに分けて処理する（サーバー等）
  - 別のプログラムを生成する
- fork, execve 関数
  - 内部ではそれぞれ clone, execve というシステムコールを呼ぶ
- 親プロセスから子プロセスへの**メモリコピーは Copy-on-Write という機能によって非常に低コスト**ですむ！
- execve
  - execve 関数を呼び出す
  - 引数で指定した実行ファイルからプログラムを読んでメモリ上に配置する（**メモリマップ**）ために必要な情報を読み出す
  - 現在のプロセスのメモリを新しいプロセスのデータで上書きする
  - プロセスを新しいプロセスの最初に実行すべき命令から実行開始する
- execve のために必要なデータ
  - コード領域のオフセット、サイズ、メモリマップ開始アドレス
  - データ領域についての情報
  - 最初に実行する命令のメモリアドレス
- Linux の実行ファイル
  - Executable and Linking Format: ELF
    - readelf というコマンドで取得可能
    - readelf -h pause
- ASLR: Address Space Layout Randomization
  - セキュリティ機能
  - **ASLR は、プログラムを実行するたびに各セクションを異なるアドレスにマップする！**
    - 攻撃対象のコードやデータが特定のアドレスに存在することを前提とした攻撃が困難になる

``` sh
# ラズパイで確認。
$ go build -o main main.go 
## executable となってる。
$ file main
main: ELF 64-bit LSB executable, ARM aarch64, version 1 (SYSV), statically linked, Go BuildID=c9iJWpjnvgcoSycVuxnJ/A3EXOKKcGdZWo3rgHd38/5CVwxX4Wbe_m7Y8NQQpG/7d89cpjJLoZbsnnrfL1z, with debug_info, not stripped

# PIE: Position Independent Executable を有効にする！
$ go build -buildmode=pie -o main main.go 
# shared object となってる。
$ file main
main: ELF 64-bit LSB shared object, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, Go BuildID=cWWzX4B-jgbXgkraVNf3/ywpwy9O6IpuBcCN3bmiB/wNRGKhUqQDCqZ2Qgp2kE/LjFYyaAFmHI2hLpB9Ef8, with debug_info, not stripped



## =========================== PIE なし ===========================
## メモリマップが全く一緒！
$ go build -o main main.go 
$ ./main &
[3] 1080609
$ cat /proc/1080609/maps
[1]   Done                    ./main
00010000-00068000 r-xp 00000000 b3:02 80288                              /home/ubuntu/work/main
00070000-000da000 r--p 00060000 b3:02 80288                              /home/ubuntu/work/main
000e0000-000e5000 rw-p 000d0000 b3:02 80288                              /home/ubuntu/work/main
000e5000-0011c000 rw-p 00000000 00:00 0 
...

$ kill -KILL 1080609
[3]+  Killed                  ./main
$ ./main &
[3] 1080779
$ cat /proc/1080779/maps
00010000-00068000 r-xp 00000000 b3:02 80288                              /home/ubuntu/work/main
00070000-000da000 r--p 00060000 b3:02 80288                              /home/ubuntu/work/main
000e0000-000e5000 rw-p 000d0000 b3:02 80288                              /home/ubuntu/work/main
000e5000-0011c000 rw-p 00000000 00:00 0 
...


## =========================== PIE あり ===========================
## /home/ubuntu/work/main の部分のメモリマップが全然違う場所になっている！
$ go build -buildmode=pie -o main main.go 
$ ./main &
[2] 1079687
$ cat /proc/1079687/maps
4000000000-4000400000 rw-p 00000000 00:00 0 
4000400000-4004000000 ---p 00000000 00:00 0 
aaaac7cb1000-aaaac7d0b000 r-xp 00000000 b3:02 80279                      /home/ubuntu/work/main
aaaac7d11000-aaaac7d3c000 r--p 00060000 b3:02 80279                      /home/ubuntu/work/main
aaaac7d41000-aaaac7d92000 r--p 00090000 b3:02 80279                      /home/ubuntu/work/main
aaaac7d92000-aaaac7d93000 rw-p 000e1000 b3:02 80279                      /home/ubuntu/work/main
aaaac7da1000-aaaac7da6000 rw-p 000f0000 b3:02 80279                      /home/ubuntu/work/main
...

$ kill -KILL 1079687
[2]+  Killed                  ./main
$ ./main &
[2] 1080050
$ cat /proc/1080050/maps
4000000000-4000400000 rw-p 00000000 00:00 0 
4000400000-4004000000 ---p 00000000 00:00 0 
aaaad74f7000-aaaad7551000 r-xp 00000000 b3:02 80279                      /home/ubuntu/work/main
aaaad7557000-aaaad7582000 r--p 00060000 b3:02 80279                      /home/ubuntu/work/main
aaaad7587000-aaaad75d8000 r--p 00090000 b3:02 80279                      /home/ubuntu/work/main
aaaad75d8000-aaaad75d9000 rw-p 000e1000 b3:02 80279                      /home/ubuntu/work/main
aaaad75e7000-aaaad75ec000 rw-p 000f0000 b3:02 80279                      /home/ubuntu/work/main
aaaad75ec000-aaaad7623000 rw-p 00000000 00:00 0 
...
```

- コンピュータ起動時の挙動
  - コンピュータの電源を入れる
  - BIOS や UEFI などのファームウェアにより、**ハードウェが初期化**される
  - ファームウェアが **GRUB などのブートローダ**を起動する
  - **ブートローダが OS カーネル**を起動する。ここでは Linux カーネルとする。
  - **Linux カーネルが init プロセス**を起動する。
    - こいつが systemd でいい！？！？！
  - init うろプロセスが子プロセスを起動し、その子プロセスが起動され、、、
- pstree
  - pstree -p
- プロセスの状態
  - ps aux
    - STAT フィールドの1文字目で判断可能
  - S
    - スリープ状態！
      - イベント待ち
  - R
    - 実行状態！か実行可能状態！
      - タイムスライスとコンテキストスイッチ
  - Z
    - ゾンビ状態！
- 全プロセスが Sleep の時？
  - **アイドルプロセス**の実行！
    - 特殊なプロセスで ps からは見えない
- ゾンビプロセス
  - **終了したが、親プロセスが終了状態を得ていない！**
  - **ゾンビプロセスが大量に存在している場合は、親プロセスに対応するプログラムのバグを疑うといい！**
- シグナル
  - あるプロセスが他のプロセスに何かを通知して、**外部から実行の流れを強制的に変える**！
  - SIGKILL
    - **シグナルハンドラによる挙動の変更はできない**
  - SIGKILL でも殺せないプロセス
    - uninterruptible sleep
      - ps aux の STAT フィールドの1文字目が D
      - ディスク I/O など
- ジョブ
  - シェルがバックグラウンドで実行したプロセスを制御するための仕組み

``` sh
sleep 411 &
[1] 39280   # [1] がジョブ番号

jobs
[1]  - running    sleep 411
[2]  + running    sleep 411

# zsh は job 番号の前に % が必要。
$ fg %1
[1]  - 39529 running    sleep 411
```

- デーモン: 常駐プロセス
  - 端末からの入出力が不要なため、端末が割り当てられていない
    - TTY フィールドが ?
      - ? は端末が結びついていないことを示す
  - あらゆるログインセッションが終了しても影響を受けないよう、独自のセッションを持つ
    - セッション ID は PID に等しい
  - デーモンを生成したプロセスがデーモンの終了を気にしなくていいよう init が親になっている
    - 親プロセスが init (PPID が 1)

## sec 3

- 2つの時間
  - 経過時間:
    - プロセスが開始してから終了するまでの経過時間
    - ストップウォッチでプロセス開始から測ったイメージ
  - 使用時間:
    - プロセスが実際に論理 CPU を使用した時間

``` sh
# real は経過時間
# user, sys は使用時間
$ time python3 load.py 
real    0m11.621s
user    0m10.689s
sys     0m0.057s  # プロセスの開始・終了時に python のインタプリタがシステムコールを呼ぶため。

# スリープ状態になるため、使用時間 ~ 0
$ time sleep 11
real    0m11.014s
user    0m0.000s
sys     0m0.014s
```

``` sh
# タイムスライスの確認。
for i in 1 2 3; do python3 sched.py $i; done

# レイテンシターゲットと呼ばれる期間に一度、CPU 時間を得られる。
$ sysctl kernel.sched_latency_ns
kernel.sched_latency_ns = 18000000  # 18 msec
```

- コンテキストスイッチ
  - 論理 CPU 上で動作するプロセスが切り替わること
  - **如何なるコードを実行中でも、タイムスライスが切れると容赦なく発生**する！
- 指標
  - ターンアラウンドタイム:
    - **システムに処理を依頼してから、個々の処理が終わるまでの時間**
  - スループット:
    - 単位時間あたりに処理を終えられる数
- わかること
  - 論理 CPU をたくさん積んでるマシンがあったとしても、そこに十分な数のプロセスを実行させて初めてスループットが向上する
  - むやみにプロセス数を増やしてもスループットは上がらない
- 並列実行の重要性
  - ムーアの法則というかシングルスレッドでの性能向上の限界 → 並列実行の重要性
