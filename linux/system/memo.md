## 全体像

- **複雑になりすぎたシステムを理解する、最も効率的な方法は、抽象化を行うこと！**
  - しびれるな
- Linux システムの3つの抽象化のレベル
  - ハードウェア
    - CPU 含
  - カーネル
    - CPU に次のタスクの場所を伝える
  - プロセス
    - カーネルが管理する実行中のプログラム
    - ユーザー空間と呼ばれるシステムの上位レベルを構成
- カーネルとプロセス
  - カーネルはカーネルモードで実行される
  - プロセスはユーザーモードで実行される
- システムコールとサポート
  - fork, exec
  - init を除いて、すべてのプロセスは fork の結果
  - **システムコールは、プロセスとカーネルの間のやり取り**


## 基本コマンド

- 多くはシステムコールと直接対応しているので、カーネルの理解を深めてくれる
- bash
  - Bourne-again shell
- I/O ストリームを使ってデータを読み書きしている！
  - 柔軟！
  - 入力ストリームは、ファイル、デバイス、ターミナルウィンドウ、他のプロセスの出力ストリーム

``` sh
man 5 passwd

info ls

# 上書きを禁止する
ubuntu@ubuntu:~$ set -C
ubuntu@ubuntu:~$ echo hoge > hoge
ubuntu@ubuntu:~$ cat hoge
hoge
ubuntu@ubuntu:~$ echo pien > hoge 
bash: hoge: cannot overwrite existing file

# c: create mode
# v: verbose
# f: file
tar cvf archive.tar file1 file2 ...
# x: extract [unpack] mode
tar xvf archive.tar
# t: table of contents
tar tvf archive.tar

$ tar tvf test.tar 
-rw-rw-r-- ubuntu/ubuntu     0 2023-05-13 04:08 a
-rw-rw-r-- ubuntu/ubuntu     0 2023-05-13 04:08 b

# .tar.gz → gz を
```




