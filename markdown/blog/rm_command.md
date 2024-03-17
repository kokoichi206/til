# rm コマンドはファイルを削除するわけではない: Linux のファイルシステム深掘り

Linux システムにおけるファイル管理は、その強力な機能性と柔軟性により、開発者やシステム管理者に広く利用されています。

多くのユーザーが頻繁に使用する rm コマンドは、ファイルを『**削除する**』と一般に認識されていますが、その背後にはより複雑なメカニズムが存在します。  
本記事では、rm コマンドが実際に何を行っているのか、そしてLinuxファイルシステムの核心概念であるinodeとディレクトリエントリについて掘り下げていきます。  
また、lnコマンドと比較することで、ファイルシステムの理解を一層深めます。

## まとめ

- inode とディレクトリエントリを分けて考える
- rm コマンドの実態は unlink システムコール
  - そのファイルを開いているプロセスが 0 の場合は実態ごと削除される
  - ln コマンドと逆の操作

**目次**

```
* [環境](#環境)
* [基本概念の理解](#基本概念の理解)
  * [ファイルシステムとは？](#ファイルシステムとは？)
  * [inode とディレクトリエントリ](#inode-とディレクトリエントリ)
* [rm コマンドの真実](#rm-コマンドの真実)
  * [システムコールから確かめる](#システムコールから確かめる)
  * [unlink システムコール](#unlink-システムコール)
* [ln コマンドとの比較](#ln-コマンドとの比較)
  * [システムコールから確かめる](#システムコールから確かめる)
```

## 環境

本記事において、コマンドの実行結果は全て以下の環境でのものです。

``` sh
ubuntu@ubuntu:~/work$ uname -a
Linux ubuntu 5.4.0-1045-raspi #49-Ubuntu SMP PREEMPT Wed Sep 29 17:49:16 UTC 2021 aarch64 aarch64 aarch64 GNU/Linux

$ $(echo $SHELL) --version
GNU bash, version 5.0.17(1)-release (aarch64-unknown-linux-gnu)
Copyright (C) 2019 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

## 基本概念の理解

### ファイルシステムとは？

ファイルシステムは、データをストレージに効率的に保存、取得、管理するための方法を提供します。  
Linux を含む多くのオペレーティングシステムでは、ファイルシステムはファイルとディレクトリ（またはフォルダ）の階層的な構造を採用しています。

この時、『ファイルの実態』と『ファイル名・パスの管理』を分けて考えることが必要です。

### inode とディレクトリエントリ

inode:  
inodeは、ファイルメタデータ（所有者、パーミッション、ファイルサイズ、データブロックへのポインタなど）を保持するデータ構造です。  
各ファイルやディレクトリは、**一意のinodeによって識別**されます。

ディレクトリエントリ:  
ディレクトリエントリは、ファイル名やディレクトリ名をその inode と結びつける役割を果たします。  
この仕組みにより、同じ inode を指す複数のディレクトリエントリ（ハードリンク）を持つことが可能になります。

## rm コマンドの真実

rm コマンドが実際に行っているのは、『ファイルのディレクトリエントリを削除すること』です。  
このプロセスにより、**ファイル名と inode の関連付けが解除されます**。  
さらに、ファイルが他のディレクトリエントリによって参照されていない、そして開かれているプロセスがない**場合に限り**、そのファイルの実体（inode とデータブロック）は削除されます。

### システムコールから確かめる

strace コマンドを使って, `rm myfile.txt` というコマンド実行に対するシステムコールを確認してみます。

``` sh
strace -o rm-test rm myfile.txt
```

全部で60行ほどの出力があったのですが, `myfile.txt` が関連してそうな箇所が後半に固まっています。

```
newfstatat(AT_FDCWD, "myfile.txt", {st_mode=S_IFREG|0664, st_size=0, ...}, AT_SYMLINK_NOFOLLOW) = 0
geteuid()                               = 1000
newfstatat(AT_FDCWD, "myfile.txt", {st_mode=S_IFREG|0664, st_size=0, ...}, AT_SYMLINK_NOFOLLOW) = 0
syscall_0x1b7(0xffffffffffffff9c, 0xaaab0c4a14d0, 0x2, 0x200, 0xffffa5e60b58, 0xffffffffffffff9c) = -1 ENOSYS (Function not implemented)
faccessat(AT_FDCWD, "myfile.txt", W_OK) = 0
unlinkat(AT_FDCWD, "myfile.txt", 0)     = 0
```

`unlinkat(AT_FDCWD, "myfile.txt", 0)` が rm の実際の動作を表しているシステムコールで、このコマンドは、myfile.txt の**ファイルエントリを削除**します。  
成功した場合（= 0）、ファイル名とinodeの関連付けが取り除かれます。この時点で、ファイルのリンクカウントがデクリメントされます。

### unlink システムコール

unlink が rm コマンドの実態であることがわかったので、もう少しコマンドについて調査しておきます。

``` sh
$ man 2 unlink

UNLINK(2)                                     System Calls Manual                                     UNLINK(2)

NAME
     unlink, unlinkat - remove directory entry
...

DESCRIPTION
     The unlink() function removes the link named by path from its directory and decrements the link count of
     the file which was referenced by the link.
     If that decrement reduces the link count of the file to zero,
     and no process has the file open, then all resources associated with the file are reclaimed.  If one or
     more process have the file open when the last link is removed, the link is removed, but the removal of the
     file is delayed until all references to it have been closed.

     ...
```

> NAME
>     unlink, unlinkat - remove directory entry

ドキュメントの概要を確認すると、『ディレクトリエントリを取り除く』みたいな感じで書いてあります。

> DESCRIPTION
>     The unlink() function removes the link named by path from its directory and decrements >the link count of
>     the file which was referenced by the link.
>     If that decrement reduces the link count of the file to zero,
>     and no process has the file open, then all resources associated with the file are reclaimed.  If one or
>     more process have the file open when the last link is removed, the link is removed, but the removal of the
>     file is delayed until all references to it have been closed.

また説明を見ると以下のことがわかります。

- ファイルのリンク数を減少させる
  - そのファイルを開いているプロセスが 0 の場合
    - 関連する全てのリソースが回収される（実態が削除される）
  - 1つ以上のプロセスがファイルを開いている場合
    - リンクは削除されるが、ファイルの削除は全ての参照が閉じられるまで遅延される

また、実は rm コマンドの man page にも『ディレクトリエントリを取り除く』と書いてあります。

``` sh
$ man rm

RM(1)                                       General Commands Manual                                       RM(1)

NAME
     rm, unlink - remove directory entries
```

## ln コマンドとの比較

ln コマンドを用いると、既存のファイルに対して新しいディレクトリエントリ（ハードリンク）を作成することができます。  
この操作では inode は共有され、ディレクトリエントリが増えるだけです。  
ln -s によるシンボリックリンク（ソフトリンク）は、実体ではなくファイル名を指し示すため、削除の挙動が異なります。

rm と ln の比較から、Linux のファイルシステムがいかにファイル名（ディレクトリエントリ）とファイルの実体（inode）を分離して扱っているかが理解できます。  
これにより、ファイルへの柔軟なアクセス方法が提供され、同時にデータの整合性とセキュリティが保たれます。

### システムコールから確かめる

strace コマンドを使って, `ln myfile.txt piyo/myfile` というコマンド実行に対するシステムコールを確認してみます。

``` sh
strace -o ln-myfile ln myfile.txt piyo/myfile
```

こちらも全部で60行ほどの出力があったのですが, `myfile.txt` が関連してそうな箇所が後半に固まっています。

```
newfstatat(AT_FDCWD, "piyo/myfile", 0xffffc04aafc8, 0) = -1 ENOENT (No such file or directory)
newfstatat(AT_FDCWD, "myfile.txt", {st_mode=S_IFREG|0664, st_size=0, ...}, AT_SYMLINK_NOFOLLOW) = 0
linkat(AT_FDCWD, "myfile.txt", AT_FDCWD, "piyo/myfile", 0) = 0
```

`linkat(AT_FDCWD, "myfile.txt", AT_FDCWD, "piyo/myfile", 0) = 0` が ln コマンドの正体（核となるシステムコール）になってます。
