## sec1

- Linux を構成する概念
  - ファイルシステム
  - プロセス
  - ストリーム


``` sh
$ gcc -dumpversion
9

gcc -o hello hello.c

# 警告オプションを全て有効にする。
gcc -o hello -Wall hello.c
```

``` c
// argv の型: char へのポインタの配列
int main(int args, char *argv[])
```

`"` はシェルの機能で、囲んだ部分を1つのコマンドライン引数にまとめる！！

- man コマンド
  - 最初に見つかったセクションのページを表示する
  - ページを指定するには
    - man 3 printf
  - section
    - 1: コマンドらいん
    - 2: システムコール 
    - 3: ライブラリ関数

## sec2

- OS
  - Linux ディストリビューション
    - シェル
    - util-lnux
    - procps
    - GNU coreutils
    - X Window System
    - GNOME, KDE
- UNIX
  - 著作権やライセンスの問題が根深く絡んでいる
  - Linux は UNIX 風 OS の一種だと考えてプログラミングできる
  - 1980
    - System V
    - BSD
      - macOS <- FreeBSD
- Linux の世界 = OS の事、ではない！
  - カーネルが作り出している世界のこと
  - **ルートディレクトリで ls した時のファイルが、カーネルのプログラム本体**
  - Linux とは OS のことだと考えられがちだが、厳密には**カーネルだけを指している**
- デバイスとデバイスドライバ
- システムコール
  - カーネルに頼み込んで仕事を依頼すること
  - ハードウェアとの直接のやり取りなど
  - システムコールこそが Linux カーネルの核心
- ライブラリ関数
  - システムコール以外に使える関数
  - ライブラリに収められているから
  - 関数を貸してもらう作業をリンクという
  - システムコールとの差は曖昧
- libc
  - Linux に用意亜sれているライブラリ
  - 標準 C ライブラリ

``` sh
ubuntu@ubuntu:~/work/hutuu$ ls /lib/aarch64-linux-gnu/libc.so.6 
/lib/aarch64-linux-gnu/libc.so.6
ubuntu@ubuntu:~/work/hutuu$ ls -l /lib/aarch64-linux-gnu/libc.so.6 
-rw-r--r-- 1 root root 1641496 Jul  6  2022 /lib/aarch64-linux-gnu/libc.so.6
```

- API
  - C のライブラリの API は関数やマクロ
  - Linux コマンドや設定ファイルが入ることも

