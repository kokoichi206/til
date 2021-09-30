## シェルの基本
シェルは、コマンドを受け付けてコンピュータに仕事をさせるソフトウェアであり、同時にプログラミング言語としての側面を有する。

C/C++, Python, AWK で作ったプログラムは「コマンド」とみなせるが、シェルはそれを組み合わせるものなので、役割の階層が違う！

### 標準入力出力エラー出力
- n>&m : n番を今m版が繋がっている（参照している）先に振り向ける、という意味
  - `sed 2>&1 | wc -l`
- |& : 標準出力も標準エラー出力もまとめて右のコマンドに渡すためのパイプ
  - `sed |& wc -l`
- 変数定義のイコールの両辺にスペースはダメ
  - a = ほげほげ、とかくと、「a をコマンドで =, ほげほげ を引数」と解釈してしまう

### シェルと変数
```sh
${a:START:CHARNUM}
${a/置換対象/置換文字}

# から文字対策として、変数はなるべくダブルクオートで囲む！
$ re=""; grep "$re" /etc/passwd
$ re=""; grep $re /etc/passwd

# ${#a} で変数の長さを取り出す
$ a=hogehoge; echo ${#a}

# set というコマンドを使うと、Bash の $1,$2,...という変数に値をセットできる
$ set aa bb cc
$ echo $2
> bb
```

### Bash の配列と連想配列
```sh
# 配列
$ a=( "$SHELL", "$LANG", "$USER")
$ echo ${a[1]}
$ echo ${a[@]}
$ echo ${#a[@]}

# 連想配列
declare -A b
b["SHELL"] ="SHELL"
b["LANG"] ="LANG"
b["USER"] ="USER"
```

### for, while
```sh
$ set aa bb cc
$ for x in "$1" "$2" "$3" ; do echo $x; done
$ seq 3 | while read x; do printf $x" "; done
$ seq 3 | while read x; do printf "%s " $x; done
```

### if
```sh
$ a=0
# これは通らない、文字に対して正しく認識しない
$ if (($a % 2 == 0)); then echo 偶数; elif (($a % 2 == 1)); then echo 奇数; else echo その他; fi
# 「条件」には、ワンライナーをそのまま書くことができる
$ if (($a % 2 == 0)); then echo 偶数; elif (($a % 2 == 1)); then echo 奇数; else echo その他; fi
# 三項間演算子ダブルで！
$ echo $a | awk '{print /[0-9]/ ? ($1%2 ? "奇数": "偶数"): "その他"}'
# exit in awk
$ echo $a | awk '/[0-9]/{print $1%2 ? "奇数": "偶数"; exit}{print "その他"}'
```

### double.bash
```sh
#!/bin/bash

if (( $# == 1 )); then
    if [[ ${1} =~ ^[0-9]*$ ]]; then
        echo $((2 * $1))
    fi
else
    echo "No arguments!"
    read input
    if [[ ${input} =~ ^[0-9]*$ ]]; then
        echo $((2 * ${input}))
    fi
fi
```

```sh
#!/bin/bash

if [ "$1" == 1 ]; then
    read n
else
    n="$1"
fi

echo $((n*2))
```

```sh
#!/bin/bash
[ "$1" = "" ] && read n || n="$1"
echo $((n*2))
```

### No.13
```sh
$ [ -e aho ] || touch aho
# <> で、「読み書きモードでファイルを開く」という意味になる
$ cat <> unfile
```

### No.14
```sh
$ for i in {1..100}; do sleep 1; echo "羊が {i}匹"; done
```

### No.15
```sh
# 全文字を大文字
 echo I am a perfect human | (read a; echo ${a^^})
I AM A PERFECT HUMAN
# 区切り文字変更＋先頭のみ大文字
$ echo I am a perfect human | (INF=" ";read -a w; echo ${w[*]^})
I Am A Perfect Human
```

### No.16
```sh
# 明示的にサブプロセスで実行させる。
## サブプロセスが作られた段階で、シェル等の変数もコピーされて渡っていく？
$ n="XYZ";(for i in {A..C}; do n+=$i; echo $n; done); echo $n
XYZA
XYZAB
XYZABC
XYZ
```

### No.17
```sh
# 先頭に空行がないファイルの場合、下でオッケー（先頭の空白が read ln で消える）
$ while read ln; do echo $ln; done < /etc/passwd
# 行頭の空白を残したい場合
$ echo "$(</etc/passwd)"
```

### No.18 お手上げ
```sh
# read {a..g} 7列を a~g の変数として受け取る
$ declare -A x; IFS=:; while read {a..g}; do x[$g]+=.; done < /etc/passwd; for s in ${!x[@]}; do echo $s ${#x[$s]}; done; unset x
/bin/bash 3
/bin/false 10
/usr/sbin/nologin 40
/bin/sync 1
```

### No.19 うーん
```sh
# <> は、ファイルの一部だけを上書きする用途で活躍できる
$ $ printf xxxx-xxxx 1<> cardno
$ a=$(<cardno); echo xxxx-xxxx-${a:10}
```

### ブレース展開, ファイルグロブ
```sh
$ echo {山,上}田
山田 上田
$ echo {1..5}.{txt,bash}
$ echo {2..10..2}.{txt,bash}
$ echo {山,上}{田,}
山田 山 上田 上

# *.png などの文字列は グロブ と呼ばれる
$ ls ?.txt  # ? は任意の1文字がマッチ
$ ls [126]5.*
$ ls [^29].*
[13-8] は、1345678 にマッチ〜
```

### No.20 ls の出力をシェルの機能で
```sh
# なぜかこれうまくいかない！
$ for i in $(cd /usr; echo *); do echo $i; done

# ## は最長一致
$ for i in /usr/*; do echo ${i##*/}; done
bin
games
include
lib
libexec
local
sbin
share
src
# # 一つは最短一致
$ for i in /usr/*; do echo ${i#*/}; done
usr/bin
usr/games
usr/include

$ a=(/usr/*); echo -e ${a[@]/\/usr\//\\n}
```

### No.21
```sh
$ find -type f

$ find -type f | sed 's@^./@@' | grep -v dir_b/d | sort
dir_a/file_1
dir_a/file_2
dir_b/file_1
dir_b/file_2
dir_c/dir_b/file_1
dir_c/dir_b/file_2

# globstar 便利！？
$ shopt -s globstar
$ echo dir_a/* dir_b/* dir_c/** | grep -o "[^ ]*[0-9]"
dir_a/file_1
dir_a/file_2
dir_b/file_1
dir_b/file_2
dir_c/dir_b/dir_a/file_1
dir_c/dir_b/file_1
dir_c/dir_b/file_2
```

### No.22
```sh
# random
$ seq 10 | sort -R
3
9
10
8
4
7
5
1
6
2
# shuf -n1 ランダムに１つ選ぶ
# shuf -n1 -e で*引数から*ランダムに１つ選ぶ
## # 13 とかは、seq を回すためだけのダミー？ # だからコメントアウト扱い？
$ seq -f 'echo $(grep -E "^[a-z]+$" /usr/share/dict/words | shuf -n1).$(shuf -n1 -e {com,org,{co.,}jp,net}) # %g' 100 | bash
```

### No.25 pipefail時の困りごと
```sh
# head は直前のコマンドを 141 = 13 = SIGPIPE のエラーで終了させる
$ seq 10000 | head
1
2
3
4
5
6
7
8
9
10
$ echo ${PIPESTATUS[@]}
141 0
# pipefail はパイプのどれかコマンド１つが終了ステータス1以上を返すと、
# そこでスクリプトを止める
set -o pipefail
```

```sh
$ trap 'rm ~/tmp/*' EXIT
```

### No.26 18時を過ぎたら帰りましょう
```sh
# 子供のプロセスが終了した時、親のプロセスが SIGCHLD を受け取る
## ビルドインコマンドには反応しない
$ trap 'echo Il offre sa confiance et son amour.' SIGCHLD
# これを .bashrc に記述すると面白い
$ trap 'h=$(date +%-H); [ "$h" -ge 18 -o "$h" -lt 3 ] && echo 早く寝ろ' SIGCHLD
```

### No.27 引数を変えてコマンドを実行
```sh
# ヒストリ置換
$ while sleep 3; do date; done
# 直前のコマンド（!!）を、3 を 1 に変えて実行
$ !!:s/3/1
# fc は履歴を編集するためのコマンド
$ fc -s 3=1
$ ^3^1
```

### No.29 静的コード解析
```sh
# 見つからないよね...
$ man bash | grep "\-n"
# 以下の -n コマンドで、実行することなく静的解析できる
## Read commands but do not execute them. 
## This may be used to check a shell script for syntax errors. 
## This is ignored by  interactive shells.
$ bash -n fb.bash
$ echo 'echo hello' | bash -n

# shred は、シュレッダーかけてくれる（じゃぁ消せ？？）
```

### No.30
```sh
# ${!hoge*} という表記は、hoge で始まる（前方一致する）変数のリストに置き換わる
$ echo ${!BASH*}
# ${変数名%%文字列}
$ set | while read s; do [[ "${s:0:4}" = 'BASH' ]] && echo ${s%%=*}; done

# プロセス置換と標準入力(-)をファイル扱いしている想定
$ set | grep ^BASH | awk -F'=' '{print $1}' | sort | diff <(echo ${!BASH*} | xargs -n 1 | sort) -   # - が大事！
```

#### set
```sh
$ set | grep BASHPID # 最初はない
$ echo $BASHPID      # 参照
$ set | grep BASHPID # 生成される
```




## 小ネタ
```sh
# 「条件」には、ワンライナーをそのまま書くことができる
$ if (($a % 2 == 0)); then echo 偶数; elif (($a % 2 == 1)); then echo 奇数; else echo その他; fi

# ポータビリティの向上
## ビルトインコマンドを呼び出すコストは、関数を呼び出すコストと同じ
$ time for i in {1..1000}; do builtin echo "$i" > /dev/null; done
real    0m0.055s
user    0m0.013s
sys     0m0.041s
# 外部 command おせえ
## 外部コマンドは、実行されるたびに新たなプロセスを生成している
$ time for i in {1..1000}; do /bin/echo "$i" > /dev/null; done
real    0m6.549s
user    0m0.773s
sys     0m5.965s

$ ps --forest
    PID TTY          TIME CMD
2303477 pts/8    00:00:06 bash
2492518 pts/8    00:00:00  \_ ps
```

- touch はファイルの時刻関連の記録であるタイムスタンプを編集するコマンド
  - touch - change file timestamps
- シェルは、プロセスとファイルを操るためのもの！！
- `$ sleep 1 | sleep 1 | sleep 1`: これは１秒で終わる
- `$ sleep 1 && sleep 1 && sleep 1`: これは３秒かかる
- fork, exec
  - fork: 完全に同じものを複製する
  - exec: あるプログラムから別のプログラムにプロセスが化ける仕組み
- 「シェルがコマンドを呼び出す」 = 「シェルが fork して、子のシェルが瞬時に exec してコマンドになる」
- ファイルディスクリプタとは、プログラムからファイルを操作する際、操作対象のファイルを識別・同定するために割り当てられる番号。
