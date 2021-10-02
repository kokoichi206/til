## パズル

### 色々な計算

```sh
# わお、bc めっちゃ正確やん
$ echo '0.1 + 0.1 + 0.1 - 0.3' | bc
0
$ echo 10000000000 + 0.0000000001 | bc
10000000000.0000000001

# awk
$ awk 'BEGIN{print 0.1 + 0.1 + 0.1 - 0.3}'
5.55112e-17
$ awk 'BEGIN{print 10000000000 + 0.0000000001}'
10000000000

# ruby の Rational クラス
$ echo '1/3 + 1/5' | sed -E 's@/.@&r@g;s/^/puts /' | ruby
8/15

# awk で素数判定
$ seq 2 99 | awk '{for(i=2; i<$1; i++){if($1%i == 0)next}; print $1}'

# エラトステネスの篩
$ seq 2 100 | xargs -I@ seq @ @ 100 | sort -n | uniq -u | xargs
```

### 組み合わせの生成
```sh
$ echo {a..c} | awk '{for(i=1; i<=3; i++)for(j=1; j<=3; j++)print $i,$j}' | awk '$1 != $2' | tr ' ' '-' | xargs
a-b a-c b-a b-c c-a c-b

# ruby, python などの用意されているものを使う
$ ruby -e 'x=["a", "b", "c"]; x.permutation(2).to_a.each do |y|; p y[0]+"-"+y[1]; end' | xargs
$ python3 -c 'import itertools; x=["a", "b", "c"]; [print("-".join(e)) for e in itertools.permutations(x, 2)]'
```

### 基数の異なる計算（cardinal number）
```sh
$ echo $(( 4#12 + 8#34 + 16#56 ))
120
$ printf "0x%x\n" $(( 4#12 + 8#34 + 16#56 ))
0x78
```

### ある数字から三角形を組める組み合わせの数
```sh
$ echo {2,3,5}{2,3,5}{2,3,5} | xargs -n 1 | awk '$1<=$2 && $2<=$3' FS= | awk '($1 + $2) > $3' FS= | wc -l
$ ruby -e '[2, 3, 5, 7].repeated_combination(3).to_a.each{|i| puts i.join(" ") if i[0]+i[1]>i[2]}'
```

### 何回紙を折ると東京から福岡まで届くか
```sh
$ yes | awk '{print 0.01*(2^NR)}' | head
0.02
0.04
0.08
0.16
0.32
0.64
1.28
2.56
5.12
10.24
$ yes | awk '0.01*(2^NR)>1000^3{print NR; exit}'
37
```

### 最初に素数になる年月日時分秒
```sh
$ seq 0 inf | sed 's/.*/2019-01-01 00:00:00 & sec/' | head
2019-01-01 00:00:00 0 sec
2019-01-01 00:00:00 1 sec
2019-01-01 00:00:00 2 sec
2019-01-01 00:00:00 3 sec
2019-01-01 00:00:00 4 sec
...
$ seq 0 inf | sed 's/.*/2019-01-01 00:00:00 & sec/' | date -f - '+%Y%m%d%H%M%S'
20190101000000
20190101000001
20190101000002
20190101000003
20190101000004
...

$ seq 0 inf | sed 's/.*/2019-01-01 00:00:00 & sec/'|\
 date -f - '+%Y%m%d%H%M%S' | factor | awk 'NF == 2{print $2; exit}'
20190101000023
```

### ラグランジュの四平方定理
```sh
# seq -w option
## -w, --equal-width: equalize width by padding with leading zeroes
$ seq -w 0 9999 | head
0000
0001
0002
$ seq -w 0 9999 | awk -F "" '{print $0, $1*$1+$2*$2+$3*$3+$4*$4}'

$ seq -w 0 9999 | awk -F "" '{print $0, $1*$1+$2*$2+$3*$3+$4*$4}' |\
 sort -k2,2n | uniq -f 1
$ seq -w 0 9999 | awk -F "" '{print $0, $1*$1+$2*$2+$3*$3+$4*$4}' | sort -k2,2n | uniq -f 1 | head -n 101
# フォーマットを整える？
$ seq -w 0 9999 | awk -F "" '{print $0, $1*$1+$2*$2+$3*$3+$4*$4}' |\
 sort -k2,2n | uniq -f 1 | head -n 101 |\
 awk -F "" '{print $1"*"$1" + "$2"*"$2" + "$3"*"$3" + "$4"*"$4" = "NR-1}'
```


### その他
```sh
# 交二進符号？
## XOR (^), 08b でゼロ埋め
$ seq 0 8 | perl -nle 'printf("%08b\n", $_ ^ $_>>1)'
$ seq 0 8 | ruby -lne 'puts "%08b" % ( $_.to_i ^ $_.to_i>>1)'
00000000
00000001
00000011
00000010
00000110
00000111
00000101
00000100
00001100
# 1列目をキーに、１列目が同じ場合に２列目を横に並べて繋げる
$ awk '{print $0,FILENAME}' user* | sort |\
 awk 'pre != $1{print ""; printf $0}pre == $1{printf " "$2}{pre = $1}' |\
 awk 'NF > 3'
```

### ポーカー
```sh
# ♧ 1 ♤ 3 ♤ 5 ♢ 10 ♡ 11 のように並んでるものとする
## カードは昇順にソートされている
# フラッシュの抽出
cat cards.txt | grep -P '^(.) (\d+)( \1 \d+){4}'

# フルハウスの抽出
## ２回目のところ、\3 であることに注意
$ cat cards.txt | grep -P '^. (\d+)( . \1){1,2} . (\d+)( . \3){1,2}$'
## 部分式呼び出しを利用
## 部分式呼び出し、後方参照と似ているがパターンだけを参照するもの
$ cat cards.txt | grep -P '^(. (\d+)( . \2){1,2}) \g<1>$'
```

### しりとり順
```sh
$ join -j9 shiritori.txt{,} | grep '\(.\) \1'
 けんこう うがい
 けんこう うしみつどき
 うがい いんどあ
 うがい いちょう
 うしみつどき きゅうけい
 いんどあ あけがた
 いちょう うがい
 いちょう うしみつどき
 きゅうけい いんどあ
 きゅうけい いちょう
# トポロジカルソートの使い所！
$ join -j9 shiritori.txt{,} | grep '\(.\) \1' | tsort 2>/dev/null
けんこう
うしみつどき
きゅうけい
いちょう
うがい
いんどあ
あけがた

## tsort
$ cat hoge 
a b
c d
b c
$ cat hoge | tsort
a
b
c
d
```

### 連続するアルファベットの検出と略記
```sh
# 目標とする出力: a-c e-f i-l p-r u w y-z
$ cat alphabet_connection
b c f i j k l p e q r u w a y z

$ cat alphabet_connection | tr ' ' '\n' | sort
# comm - <(), 標準入力をファイル入力にする - とコマンド置換
$ cat alphabet_connection | tr ' ' '\n' | sort |\
 comm - <(echo {a..z} | tr ' ' '\n') | sed 's/^..//'
# 略記にする（a\nb\nc -> a-c\n）
$ cat alphabet_connection | tr ' ' '\n' | sort |\
 comm - <(echo {a..z} | tr ' ' '\n') | sed 's/^..//g' |\
 sed -zE 's/([a-z])(\n[a-z])*\n([a-z])/\1-\3/g'
# 横に並べて完成
$ cat alphabet_connection | tr ' ' '\n' | sort |\
 comm - <(echo {a..z} | tr ' ' '\n') | sed 's/^..//g' |\
 sed -zE 's/([a-z])(\n[a-z])*\n([a-z])/\1-\3/g' | xargs
a-c e-f i-l p-r u w y-z

# 別解
1$ cat alphabet_connection | tr ' ' '\n' |\
 (cat; echo {a..z} | tr ' ' '\n') | sort  | uniq -c |\
  awk '$1 == 1{print ""}$1 == 2{printf $2" "}' |\
   awk 'NF==1{print $1}NF>1{print $1"-"$NF}' | xargs
```

### クワイン
```sh
# $BASH_COMMAND はデバッグに使えるなぁ
## trap 'echo "$BASH_COMMAND"' ERR
$ echo $BASH_COMMAND

```


## 小ネタ
- awk の next: その行の処理を打ち切って次の行に行くときに使う！
- 先頭が 0 の場合 8 進数、0x の場合 16 進数と解釈される
