# シェル芸勉強会

## utf code in shell

```
echo ぺ | iconv -f utf8 -t ucs2 | xxd -p
echo -e \\U307b
echo -e \\U307b\\U309A
```

「ほ＋◯」と「ぽ」は別物
```
echo -e a\\U3099
echo -e a\\U309A
```

## prime
```
factor 127 | awk NF==2
```
シェルが存在しないコマンドの終了ステータスが127

```
echo $? -> 127
( _ ; echo $? ) |& grep -v _
```

$$で、場所のプロセス番号を指定している。よって
```
$$/$$ = 1
```

それをビットシフトすると2ができる
```
echo $(($$/$$<<$$/$$))
```

final
```
( _ ; echo $? ) |& grep -v _|factor | awk NF==$(($$/$$<<$$/$$))
```

```
${#}
```
で変数の数なので、変数の数の数は1になる！

```
${##} = 1
```

## grep
.で1文字ずつ、-oでその文字を毎行出してくれっていう意味
無限チキチキボーン
```
yes $(<chiki) | grep -o .
```

適当なところで止める
```
grep -o . updown | paste - <(yes $(<chiki) | grep -o .) | head -n 20
```

up,downによって左右分ける、
```
grep -o . updown | paste - <(yes $(<chiki) | grep -o .) | head -n 20 | sed -E 's/v.*(.)$/\1 v @/' | sed -E 's/\^/@ ^/' | tr \\t ' '
```

echo 1 2 3 4 5 6 | xargs -n 3
-o only matching
-P --perl-regexp

## htmlのなかのタグの数を数える
```
cat aho.html | grep -oE -e '<[a-z]+ ' -e '[a-z]+>' | tr -d '<> ' | sort -u
```
```
grep span aho.html
grep -n span aho.html
```

## キャプション of markdown
A[^about_a]は素晴らしい

[^about_a]:Aの起源は室町時代に

### これを、tex用の\footnote{...}に変えよう
変えたいのは、annotation.md のもの
```
cat annotation.md | awk '/^\[/{print $1, "\\\\footnote{"$2"}"}'
```
[]のエスケープが難しい？
markdown をコマンドでいじるのは工夫が必要
```
cat annotation.md | awk '/^\[/{print $1, "\\\\footnote{"$2"}"}' | sed 's/^/s;/' | sed 's/: /;/' | sed 's/$/;/' | sed 's;\[;\\[;' | sed 's;\^;\\^;' | sed 's;\];\\];' | sed -f- annotation.md
```
\と正規表現を全部エスケープする
sedの命令のメタ文字を全部エスケープ〜〜
### sed 
-f- で標準入力からsedの入力を受け取る、っていう命令になる
```
cat annotation.md | grep '^\[' | awk '{print $1,"\\\\footnote{"$2"}"}' | sed 's/\[/s;\\[/' | sed 's;\^;\\^;' | sed 's;\];\\];' | sed 's/: /;/' | sed 's/$/;/' | sed -f- annotation.md | grep -v '^\\footnote'
```
```
grep -v '^\\footnote
```
で、footnoteから始まるものを削除している

## （texで）重複行をチェック
1〜3行目と100〜102行目がまったく同じ、などということがあった場合、それを検知して報告する

tabやspaceを、awkで処理しやすいように__に変換
```
tr '\t ' '__'
```
空白を消すついでに行番号を出す
```
awk '!/^$/{print NR,$0}'
```
2つめ（テキストの内容）でsortする、-k2
```
sort -k2,2
```
-f1で1列目を無視してuniq取ってくれる
-Dで重複した行を両方出してくれる
```
uniq -f1 -D
```

final
```
cat contents.tex | tr '\t ' '__' | awk '!/^$/{print NR,$0}' | sort -k2,2 | uniq -f1 -D | grep -Ev '\\(begin|end){(bmatrix|align|figure|center)}' | sort -k1,1n
```

## ls
```
ls -atlr
```

## 1から1億までの数字をシャッフルして2列にしたデータを作る（ファイル名'a'）
一番素直なもの
```
time seq 100000000 | shuf | xargs -n 2 > a
```
shuf: memory exhausted
と言われた。
```
time seq 10000 | shuf | xargs -n 2 > a
```

結論
**pasteがはやい**
```
time seq 100000 | shuf | paste - - | tr \\t ' ' > a
```
**awk**は遅い
```
time seq 100000 | shuf | awk 'NR%2==1{printf $1" "}NR%2==0{print $1}' | head
```
高機能になるほど遅い
paste -d' ' - - - 


これでも全然無理。xargsは全然駄目、いかに普段小さいデータしか使ってないか

並列化処理とかやろうとしても無理でした。
```
time seq 1000000 | awk '{if(rand() > 0.5){print $1 > "x"}else{print $1 > "y"}}'
wc -l x y
```
これ、どこにx,y保存されてるん？ナニコレ

```
time (seq 100000 | awk '{if(rand() > 0.5){print $1 > "x"}else{print $1 > "y"}}'; echo x y | tr ' ' \\n | xargs -n 1 -P0 shuf | paste - - )
```
なぜかこれより以下のワンステップ加えた方が速い
```
time (seq 100000 | awk '{if(rand() > 0.5){print $1 > "x"}else{print $1 > "y"}}'; echo x y | tr ' ' \\n | xargs -n 1 -P0 shuf | paste - - | awk '{print $1,$2}')
```

## これを2列目を基準にsortしなおす
```
cat a | sort -k2,2n > b
sort -k2,2n a > b
```
したの方が速い。catを使うとシングルスレッドにしかならない。何故か
```
time tac a > /dev/null
cat a | tac > /dev/null
```
も同じことが言える

## 'a'について、両方の数字が素数の業を抽出してファイルに保存する
```
cat a | factor | paste - - | head
```
ans
```
time cat a | factor | paste - - | awk 'NF==4{print $2,$4}' > hoge
time cat a | awk '$1%2 && $2%2' | factor | paste - - | awk 'NF==4{print $2,$4}' > hoge2
```

## 'a'を各行にA..Zをつけて、各アルファベットごとに並べる
```
time yes {A..Z} | tr ' ' \\n | paste - a | head -n 50000
```
ここからどうするか？小さいデータならawkでくっつけたらいいけど、それだとメモリーが足りなそう
2、3行目を1行目の名前のファイルに書き出す
```
time yes {A..Z} | tr ' ' \\n | paste - a | head -n 50000 | awk '{printf $2" " > $1; printf $3" " > $1}'
```
これを再びくっつける
```
grep . {A..Z} | tr : ' ' > ans
awk '{print NF}' ans
```
まとめると？？
いっぱい列あるソートは、LANGとか-sとかつけとくとはやくなるきする
```
time ( yes {A..Z} | tr ' ' \\n | paste - a | head -n 50000 > tmp; LANG=C sort -s -k1,1 tmp > tmp2 )
```
ファイルにまとめるといいことがある。
## このA、B、、、Zごとにsortすると？
とりあえず
```
echo {A..Z} | tr ' ' \\n | xargs -I@ echo @
```
xargs -P0 でCPU全部使って並列化して処理する！！！
また、xargsはbash -cをつけると便利
paste -sd' 'で再び1行に戻す
```
cat A | tr ' ' '\n' | sort -n  | paste -sd' '
```
ans
```
echo {A..Z} | tr ' ' \\n | xargs -I@ -P0 bash -c "cat @ | tr ' ' '\n' | sort -n | paste -sd' ' > s@ "; grep . s{A..Z} | tr -d s > ans2
```
確かめ
```
awk '{print $1,$2,$3, "...", $(NF-1),$NF}' ans2
```

## print あ
```
ls aaaa |& rev
```
unicodeを利用
```
echo -n い | xxd -ps | awk -F '' '{$NF-=2;print }'
echo -n い | xxd -ps | awk -F '' '{$NF-=2;print }' | tr -d ' ' | xxd -p -r | awk 4
echo -e \\U$((2*3*3*13*13))
```

## ls
```
find * -printf '%p %Tc\n' | column -t
echo * | xargs -n 1 stat | grep -e '^ *File' -e '^Modify' | awk '{$1="";print}' | xargs -n 4
```

## seq 30から3のつく数だけ取り出す
```
seq 30 | sed '/3/!d'
seq 30 | awk /3/
```

## 3+4+5+6
```
echo 3+4+5+6 | grep -o . | xargs expr
echo 3+4+5+6 | python3 -c 'import sys;a=[e for e in sys.stdin ];print(a[0].rstrip().split("+"))'
echo 3+4+5+6 | python3 -c 'import sys;a=[e for e in sys.stdin ];b=a[0].rstrip().split("+");[ print("."*int(s)) for s in b]'
echo 3+4+5+6 | python3 -c 'import sys;a=[e for e in sys.stdin ];b=a[0].rstrip().split("+");[ print("."*int(s))   for s in b]' | grep -o . | wc -l
```
sleep
```
echo 3+4+5+6 | tr + \\n | time xargs -n 1 sleep |& head -n 1 | awk '{print $3}' | sed 's/\..*//' | sed 's/0://'
```

## rev
```
echo てぶくろ | grep -o . | while read w ; do a=$w$a; echo $a; done | tail -n 1
echo てぶくろ | rev
echo てぶくろ | grep -o . | awk '{print "sleep", 5-NR, "&& echo", $1, "&"}' |bash
```

## is_prime
```
seq 9 | tr -d \\n | grep -o .. | awk '{print "0x"$1}' | xargs printf "%d\n"
```

## number 0 to 9
```
seq $? inf | head
cat /etc/passwd | nl | grep -oP '.\t' | head | sort

```
nl, numberling?

## unicode
unicodeは字形を区別して登録しない！？
すべてのaは同じa？？
The Unicode Consortium
文字、グリフ、フォントを指定して文字を登録する


## memo
### ファイルキャッシュ
普段使ってるようなファイルは、SSDじゃなくてDRAMの上にのってて読み出してるから、早く読めるようなシステムになってる。
8gと16gのメモリでは、アプリをそんなに使ってなくても、スピードの使用感は全然異なる。
このようにファイルキャッシュをのせるために、多いメモリを選ぶのはよい。
GUIのアプリを開きすぎるとファイルキャッシュが効かなくなり遅くなる、グラフィックなIDEには注意！
#### キャッシュファイルのけしかた
```
echo 1 | sudo tee /proc/sys/vm/drop_caches
time cat hoge > /dev/null
```

### 略語
- NF .. Number of Field




## sed
- [example](https://www.folkstalk.com/2012/01/sed-command-in-unix-examples.html)

### s///
のsは置換

### ///g
のgはすべてのものに対し、っていう意味
/a//3なら3番目のaに対し処理を行う

### '/a/d'
のdをこういう風に書くと、削除の意味

### sed -r
の-rは正規表現

## 5行先のものとたす
```
seq 1000 | shuf > aho
paste aho aho
paste aho <(sed 1,5d aho)
paste aho <(sed 1,5d aho)| head 
paste aho <(sed 1,5d aho)| tail
paste aho <(sed 1,5d aho)| awk 'NF==2' | tail
paste aho <(sed 1,5d aho)| awk 'NF==2' | awk '{print $1,$1+$2}' | head
paste aho <(tail -n +6 aho) | head
```

## 1列目を2列目で割って約分する
```
cat frac
> 123 42
cat frac | factor | awk 'NR==1{for(i=2;i<=NF;i++)a[$i]++}END{for(k in a){print k,a[k]}}'
cat frac | factor | awk 'NR==1{for(i=2;i<=NF;i++)a[$i]++}NR==2{for(i=2;i<=NF;i++)a[$i]--}END{for(k in a){print k,a[k]}}'
cat frac | factor | awk 'NR==1{for(i=2;i<=NF;i++)a[$i]++}NR==2{for(i=2;i<=NF;i++)a[$i]--}END{for(k in a){print k,a[k]}}' | awk 'BEGIN{a=1;b=1}$2>0{a*=$1^$2}$2<0{b*=$1^(-$2)}END{print a,b}'
```

## 1番下の桁を四捨五入する
```
cat nums
-0.37 2.333333 4.0000099995
cat nums | awk '{print length}'
cat nums | awk -F '' '$NF>=5{$(NF-1)++}{$NF="";print}'
cat nums | awk -F '' '$NF>=5{$(NF-1)++}{$NF="";print}' | awk '{while($NF==10){$(NF-1)++;$NF="";NF--};print}' | tr -d ' '
```
この方法は有名？
```
echo 0.49 | awk '{print int(($1+0.05)*10)/10}'
``` 

### 切り捨て
```
cat nums | awk -F '' '{$NF="";print}'
```

## 九九の表を作る
```
echo {1..9}{1..9} | tr ' ' '\n' | awk -F '' '{printf"%2s\n",$1*$2}' | paste -d ' ' - - - - - - - - - 
```

## 4桁のなんとか
```
echo 1987 | awk -F '' '{for(i=1;i<=4;i++){a[i]=$i};asort(a,x);for(i=1;i<=4;i++){b=x[i]b;c=c x[i]};print b,c;$1=b-c;print $1}'
echo 987 | awk -F '' '{$0=sprintf("%04d",$0);print $0;for(i=1;i<=4;i++){a[i]=$i};asort(a,x);for(i=1;i<=4;i++){b=x[i]b;c=c x[i]};print b,c;$1=b-c;print $1}'
echo 1 | awk -F '' '{while(1){b="";c="";$0=sprintf("%04d",$0);for(i=1;i<=4;i++){a[i]=substr($0,i,1)};asort(a,x);for(i=1;i<=4;i++){b=x[i]b;c=c x[i]};$0=b-c;print $0}}' | uniq
```

### awk
- sort, asort(a, x), aをソートしてxという名前に保存
- string の i 番目を取り出す
    - a[i]=substr($0,i,1)

## 素数の何とか
- 改行なしで出力したい
    - printf を使う

```
while :; do seq 1 1000 | factor | awk 'NF==2{print $2}' | shuf | head -n 2 | sort -n | tr \\n ' ' | awk '{printf $1" "$2" "};{for(i=1;i<=4;i++){printf $2+($2-$1)*i" "}}END{print " "}'; done | head -n 5
```
```
while : ; do seq inf | factor | awk 'NF==2{print $2}' | head -n 1000 | shuf -n 2 | sort -n | paste - - | awk '{d=$2-$1;for(i=0;i<6;i++)printf $1+d*i " ";print ""}'; done
```

### 素数生成
```
seq 1 inf | factor | awk 'NF==2{print $2}' | head
```

### タイマー、コマンドラインでの無限ループ
```
t=1;while :;do sleep 1 | echo $t && t=$(($t+1)) ;done
```

### sort
数字でソート
sort -n

### 500 行くらい、適当にファイルに保存
```
i=1; while [ "$i" -lt 500 ] ; do seq inf | factor | awk 'NF==2{print $2}' | head -n 1000 | shuf -n 2 | sort -n | paste - - | awk '{d=$2-$1;for(i=0;i<6;i++)printf $1+d*i " ";print ""}' >> primes.txt && i=$(($i+1)); done
```

### すべてが素数のものだけを出力
- この数列は、等差数列かつすべてが素数のもの！
    - 6 だけじゃなくて、すべての数列の数に対して存在する！！

```
cat primes.txt | factor | awk '{print int((NR-1)/6),NF}' | awk '$2==2' | awk '{a[$1]++}END{for(k in a)print k,a[k]}' | awk '$2==6{print $1}' | xargs -I@ sed -n '@p' primes.txt
```

sed -n 6p fileName


### 長すぎるコマンド
- バッファが詰まることがある
- 解消方法の例
    - awk: fflush
    - sed -u, unbuffered


## フラクタルを書く！
triangleから出発してコッホ曲線

### 三角形を書く
```
cat triangle
50 86.6025
100 0
0 0
```
のファイルに対して
```
cat triangle | gnuplot -e 'set terminal png;set size ratio -1;set output "./hoge.png";plot "-" w l'
```

### いっかいのもの
```
cat triangle | awk 'NR==1{x1=$1;y1=$2}NR>1{x5=$1;y5=$2;l=sqrt( (x5-x1)^2 + (y5-y1)^2 )/3;a=atan2(y5-y1,x5-x1);x2=x1+l*cos(a);y2=y1+l*sin(a);x3=x2+l*cos(a+3.141592/3);y3=y2+l*sin(a+3.14159265/3);x4=x5-l*cos(a);y4=y5-l*sin(a);print x1,y1;print x2,y2; print x3,y3; print x4,y4 ;x1=x5;y1=y5}END{print x1,y1}'| gnuplot -e 'set terminal png;set size ratio -1;set output "./hoge.png";plot "-" w l'
```

### 任意の回数のコッホ曲線を書く
```
for i in {1..20}; do cat koch/triangle$i | awk 'NR==1{x1=$1;y1=$2}NR>1{x5=$1;y5=$2;l=sqrt( (x5-x1)^2 + (y5-y1)^2 )/3;a=atan2(y5-y1,x5-x1);x2=x1+l*cos(a);y2=y1+l*sin(a);x3=x2+l*cos(a+3.141592/3);y3=y2+l*sin(a+3.14159265/3);x4=x5-l*cos(a);y4=y5-l*sin(a);print x1,y1;print x2,y2; print x3,y3; print x4,y4 ;x1=x5;y1=y5}END{print x1,y1}' > koch/triangle$(($i+1)) && echo $i; done
```





