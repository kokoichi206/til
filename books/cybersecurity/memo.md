# メモ

## sec1
実行可能なコマンド３つ

- ファイル
- 組み込みコマンド（built-in）
  - 高速
- 予約後（keyword）

```sh
$ type -t if
keyword
$ type -t pwd
builtin

# -k: 予約語 -c: コマンド -b: builtin
$ compgen -k
```

標準入出力のリダイレクト

```sh
$ handywork < data.in > results.out 2> err.msgs
$ handywork < data.in > results.out 2>&1
# これは上と一緒
$ handywork < data.in &> results.out

# 追記にしたい時
$ handywork < data.in &>> results.out
```

コマンドのバックグラウンド実行
```sh
$ ping 8.8.8.8 &> ping.log &
$ jobs
$ fg TASK_NUM
```


## sec2
variable 

"の中では変数は展開される！
'の中ではされない！

次のように、$()という構文を用いることで、コマンドの出力を変数に格納できる

```sh
$ C=$(pwd)
$ echo $C
/home/ubuntu/work

$ D=`pwd`
$ echo $D
/home/ubuntu/work
```

条件

コマンドやプログラムは成功や失敗を表す値を常に返却する。それは`$?`という変数で参照できる

0が「成功（真）」で、それ以外の値は「失敗（偽）」であることに注意すること（ただし、(())のなかは例外？？）

```sh
if cd /tmp
then
    echo "here is what is in /tmp:"
    ls -l
fi
```

パイプは**最後のコマンドの**返却する成功もしくは失敗の値で決定される

```sh
if ls | grep pdf
then
    echo "found one or more pdf files here"
else
    echo "no pdf files found"
fi
```

上で条件を`ls | grep pdf | wc`とやると、真になる！

数値評価演算子には`-eq, -gt, -lt`を用いる！

\> を使うと、辞書順での評価になる！

```sh
if [[ $VAL -lt $MIN ]]
then
    echo "value is too small"
fi
```

もしくは、(())を用いる！

(())の中では、より数値的な処理が行われる（1がTrueなど、他の言語に近い）

変数を参照する$も不要

```sh
if (( VAL < 12 ))
then
    echo "value $VAL is too small"
fi
```

```sh
$ [[ -d $DIR ]] && ls "$DIR"

# 同じ意味
if [[ -d $DIR ]]
then
    ls "$DIR"
fi
```

loopを行う際のグルーピングは、`do; done`という予約語

```sh
while ls | grep -q pdf
do
    echo -n 'there is a file with pdf in its name here: '
    pwd
    cd ..
done
```

一連の数字を生成する
```sh
{1..10}
{090..104..2}
```

関数は現在のシェルではなく、**サブシェル**え実行される。したがって、グローバル変数への変更はサブシェルの中でのみ反映され、メインのシェルには反映されない、変更した内容は消失する


bashシェルの強み

- 他のプログラムを簡単に起動できる
- 一連のプログラムの実行結果を連携できる

