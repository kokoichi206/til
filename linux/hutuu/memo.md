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

