# blog
[上田さんのブログ](https://b.ueda.tech/?page=00684)から勉強させてもらったもの

## 各コマンドメモとか

### 連想配列
[Q]
```bash
$ cat data1
a 1
b 4
a 2
a 3
b 5

# 期待される出力
a 1 2 3
b 4 5
# もしくは
{a:[1,2,3],b:[4,5]}
```
[A]
```bash
$ cat data1 | awk '{d[$1]=d[$1]" "$2}END{for(k in d){print k d[k]}}' 
```
JSONにするには
```bash
cat data1 | awk '{d[$1]=d[$1]" "$2}END{for(k in d){print k d[k]}}' |
 awk -v q='"' '{printf q$1q":[";for(i=2;i<=NF;i++){printf $i","};print "]"}'| xargs | tr ' ' ',' | awk '{print "{"$0"}"}' | sed 's@,]@]@g'
```

### sed
置換オプションの時に、該当文字を置換後の中にも使いたい時は、&を使う！
```bash
# aがきたら改行する(aを残しつつ)
$ echo hogeafugapien | sed 's/a/&\n/g'
```

0012 -> 12 などにする（先頭の0を取り除いて数字にする）
```bash
# *は0個以上（最長一致）
$ echo 0012 | sed 's/^0*//'
```

### awk
部分文字列取得 - substr（１オリジンに注意！）
```bash
$ echo hoge | awk '{print substr($1, length($1), length($1))}'
$ echo 1234 | awk '{print substr($1, length($1), length($1))}'
```

awk内部でシェルコマンドを使いたい！（system.）
```bash
yes '*'| awk 'BEGIN{a="*"}{print a;a=a$1};system("sleep 1")' | xargs -I@ echo @
```


### grep

#### options
- -L, --files-without-match


### tac, rs
- tac - concatenate and print files in reverse
- rs - reshape

```bash
$ echo -e 'a b\nc d'       
a b
c d
$ echo -e 'a b\nc d' | tac
c d
a b
$ echo -e 'a b\nc d' | rs -T
a  c
b  d
```


## 問題！
[Q]
ファイルの中に3個存在する文字を出力してください
```bash
$ cat 8q4
aabbcdabbcccdd
```

[A]
```bash
$ cat hoge | sed 's/./&\\n/g' | awk 'NF==1' |
 sort | uniq -c | awk '$1==3{print $2}'
a
d
```

[Q]
0から999999までの数字の一様乱数を無限に出力する

[A]
```bash
$ cat /dev/random | gtr -dc 0-9 | gfold -b4 | sed 's@^0*@@'
```

[Q]
上の乱数の下１桁が同じものでまとめて、その数調べる
```bash
# とりあえず連想配列に0をぶち込んだ
# 変数使うとき、先頭に$とか何もいらないんだ..
$ cat /dev/random | gtr -dc 0-9 | gfold -b4 | sed 's@^0*@@' | head -n 10000 \
| awk 'BEGIN{for(i=0;i<=9;i++){a[i]=0}}{v=substr($1,length($1),length($1)); a[v]=a[v]+1}END{for(i=0;i<=9;i++){print i" "a[i]}}'
```

[Q]
下のような入力から、抜けた数字の行は飛ばして出力させる
```bash
echo 14679
```

[A]
```bash
echo 147679 | sed 's/./&\n/g' | awk '{a[$1]=$1}END{for(i=0;i<=9;i++){print a[i]}}'
```

[Q]
8128が完全数であることを確認してください

[A]
```sh
seq 2 8128 | awk '{print 8128/$1}' | grep -Fv . | tr '\n' + | sed 's@\+$@\n@'| bc
```


