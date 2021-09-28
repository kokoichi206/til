## sec 1
- コマンドを２つ以上組み合わせたものは、一般的にワンライナーと呼ばれる
- パイプにコマンドが繋がったものを指して、パイプラインと呼ぶこともある

### sed
```bash
# 基本正規表現で、マッチしたものを引用する！
# → &
$ echo '1+1' | sed 's/./& /g' # -> 1 + 1
```

### perl
```bash
$ echo '1+1' | perl -e '{printf "%d\n", eval(<STDIN>)}'
```

### grep
```bash
$ seq 100 | grep "[02468]$" | xargs
$ seq 100 | grep "[^02468]$" | xargs
$ seq 100 | grep "7." | xargs

seq 5 | grep -v 3
1
2
4
5
# -R ディレクトリの中を再帰的に読み込む
# -l 検索結果を表示せずにファイル名だけを出力する
$ grep -l '^10$' -R | rm
$ time seq 100000 | xargs -P2 grep '^10$' -l
```

### awk
- awk は grep にプログラム機能をつけたもの
- パターン（条件）とアクション（処理）で記述
- 暗黙的に変数は 0 で初期化されて始まる

```bash
# 正規表現
$ seq 5 | awk '/[02468]$/'
$ seq 5 | awk '$0 % 2 == 0'
$ seq 5 | awk '/[02468]$/{printf $0" 偶数\n"}'
$ seq 5 | awk '/[02468]$/{printf $0" 偶数\n"}/[13579]$/{printf $0" 奇数\n"}'
$ seq 5 | awk 'BEGIN{a = 0}/[02468]$/{printf $0" 偶数\n"}/[13579]$/{printf $0" 奇数\n"}{a += $0}END{print "合計 "a}'

$ seq 5 | awk '{print $1 % 2}' | sort -r | uniq -c | awk '$2{print("奇数",$1)}$2 == 0{print("偶数",$1)}'
$ seq 5 | awk '{print $1%2 ? "奇数": "偶数"}'
```

### xargs
```bash
# 横に並べることができる
$ seq 4 | xargs -n2
$ seq 4 | xargs -n2 mv
$ seq 4 | xargs -I@ mkdir dir_@
```

### bash
```bash
$ seq 4 | awk '{print "mkdir "($1%2 ? "odd_": "even_")$1}' | bash
$ ls -d odd_* even_*
```


### その他
```bash
$ nautilus
# ２列めから２列めをソート
$ sort -k2,2
```

### ファイル
```bash
$ find . -name files.txt

$ find . -name files.* | xargs cat | grep .exe
# メタ文字 . を \ でエスケープ。\ はエスケープ文字と呼ばれる
$ grep '\.exe$' files.txt
```

### image
```bash
$ sudo apt install imagemagick
$ convert a.png b.jpg
$ file b.jpg
$ ls *.png | tr -d '.png' | xargs -I@ convert @.png @.jpg
# xargs -P2 などで高速化
# -P2 はプロセスの数。並列実行
$ ls *.png | sed 's/\.png//' | xargs -P2 -I@ convert @.png @.jpg
```

### parallel
```bash
$ sudo apt install parallel
# {} がファイル名、{.} がファイル名から拡張子を除いたもの
$ time parallel 'convert {} {.}.jpg' ::: *.png

$ parallel 'echo {}' ::: *.png
```

### file
```bash
$ seq 1000000 | xargs -P4 touch
# ls は標準でファイルのソートが入ってしまう
$ time ls
real    0m45.936s
user    0m10.988s
sys     0m22.265s
# ソートしない
$ time ls -U

# find の方が ls より高速？
$ time find
real    0m36.565s
user    0m4.820s
sys     0m18.777s

# rename (0 fill)
$ time ls -U | xargs -P2 rename 's/^/0000000/;s/0*([0-9]{7})/$1/'
real    50m56.146s
user    0m43.495s
sys     2m38.924s
```


### 1-5
```sh
$ cat ntp.conf | awk '$1 == "pool"{print $2}' | sed -E 's@[0-9]*\.?(.*)@\1@g'
```

### 1-6
```sh
$ seq 5 | awk '{for(i=0; i<5-$1; i++){printf " "}}{print "×"}'
$ seq 5 | awk '{for(i=0; i<$1; i++){printf " "}}{print "×"}' | tac
$ echo -e "    x\n   x\n  x\n x\nx"
# seq をそもそも逆にする
$ seq 5 -1 1   # seq START STEP END, seq 5 = seq 1 1 5
$ printf "%*s\n" 5 x 4 x 3 x 2 x 1 x
# sed のラベル機能
## a: 前の命令が成功したらラベルaに戻る
## p: print, s: 空白を１つ削除, 最後のd: 残った文字列を削除
$ echo '    x' | sed ':a;p;s/ //;ta;d'
```

### 1-7
```sh
$ cat kakeibo.txt | awk '{tax = ($1 < "20191001" || $2 ~ "^*") ? 1.08 : 1.1; print $0, tax}'
$ cat kakeibo.txt | awk '{tax = ($1 < "20191001" || $2 ~ "^*") ? 1.08 : 1.1; print $0, tax}' | awk '{print int($3*$4); sum += int($3*$4)}END{print("合計:", sum)}'
# numsum 便利
$ cat kakeibo.txt | awk '{tax = ($1 < "20191001" || $2 ~ "^*") ? 1.08 : 1.1; print $0, tax}' | awk '{print int($3*$4)}' | numsum
```

### 1-8
```sh
$ cat access.log 
183.YY.129.XX - - [07/Nov/2017:22:37:38 +0900]
192.Y.220.XXX - - [08/Nov/2017:02:17:16 +0900]
66.YYY.79.XXX - - [07/Nov/2017:14:42:48 +0900]
::1 - - [07/Nov/2017:13:37:54 +0900]
133.YY.23.XX - - [07/Nov/2017:09:41:48 +0900]

$ awk -F: '{print $(NF-2)}' access.log | awk '$1 < 12{print "午前"} $1 >= 12{print "午後"}' | sort | uniq -c
$ cat access.log | grep -o '..:..:.. +0900' | sed 's/:.*//'
# sed は続けてかける！
## | は拡張正規表現における OR にあたる！
$ sed -r 's@.*\[|\]|/@@g' access.log 
07Nov2017:22:37:38 +0900
08Nov2017:02:17:16 +0900
07Nov2017:14:42:48 +0900
07Nov2017:13:37:54 +0900
07Nov2017:09:41:48 +0900
$ sed -r 's@.*\[|\]|/@@g;s/:/ /' access.log
07Nov2017 22:37:38 +0900
08Nov2017 02:17:16 +0900
07Nov2017 14:42:48 +0900
07Nov2017 13:37:54 +0900
07Nov2017 09:41:48 +0900

# date
$ date %+H+p
$ date "+%Y%m%d %H%M%S"
20210928 115212
```

### 1-9
```sh
$ cat log_range.log | head
192.168.60.74 - - [01/Dec/2016 00:20:09] "GET / HTTP/1.0" 200 5855
192.168.49.206 - - [01/Dec/2016 01:04:29] "GET / HTTP/1.0" 200 1518
192.168.93.125 - - [01/Dec/2016 02:21:15] "GET / HTTP/1.0" 200 8931
192.168.56.161 - - [01/Dec/2016 03:13:19] "GET / HTTP/1.0" 200 1044
192.168.128.144 - - [01/Dec/2016 04:20:02] "GET / HTTP/1.0" 200 1080
192.168.163.3 - - [01/Dec/2016 05:17:06] "GET / HTTP/1.0" 200 4829
192.168.64.172 - - [01/Dec/2016 06:21:45] "GET / HTTP/1.0" 200 7202
192.168.231.236 - - [01/Dec/2016 07:09:53] "GET / HTTP/1.0" 200 7788
192.168.82.49 - - [01/Dec/2016 08:23:09] "GET / HTTP/1.0" 200 7080

$ cat log_range.log | grep Dec/2016 | awk '(substr($4,2,12) == "24/Dec/2016" && substr($5,1,2) >=21) || (substr($4,2,12) == "25/Dec/2016" && substr($5,1,2) <= "03")'

# sed -n '/正規表現1/,/正規表現2/p' 1にマッチする列から2にマッチする列まで！
## これは、その間がマッチしていなくても出してくれる！
$ seq 10 | awk '{print $1%5}' | sed -n '/2/,/4/p'
2
3
4
2
3
4
$ cat log_range.log | sed -n '/24\/Dec\/2016 21:..:../,/25\/Dec\/2016 03:..:../p'
# awk でも同じようなことができる！
$ cat log_range.log | awk '/24\/Dec\/2016 21:..:../,/25\/Dec\/2016 03:..:../'
```

### 1-10
Markdown, Atx 形式と Setext 形式がある！

Atx がよくみる方

```sh
$ cat headings.md | sed -E 's@^# (.*)@\1\n===@g;s@^## (.*)@\1\n---@'
```

### 1-11

```sh
$ cat gijiroku.txt | sed -z 's/すず\n/鈴木:/g; s/さと\n/佐藤:/g; s/やま\n/山田:/g'
$ cat gijiroku.txt | xargs -n2 | sed 's/すず/鈴木:/g; s/さと/佐藤:/g; s/^やま/山田:/g; s/$/\n/'
```


## 小ネタ
```bash
# awk で三項間演算子使える
$ seq 4 | awk '{print "mkdir "($1%2 ? "odd_": "even_")$1}'
# sed -n で一致したところ**のみ** print
# sed -n '/正規表現/p'
$ find . -name files.* | xargs cat | sed -n '/\.exe$/p'
$ find . -name files.* | xargs cat | awk '/\.exe$/'
# sed は続けてかける！！
$ sed -r 's@.*\[|\]|/@@g;s/:/ /' access.log
# sed -n '/正規表現1/,/正規表現2/p' 1にマッチする行から2にマッチする行を表示
$ cat log_range.log | sed -n '/24\/Dec\/2016 21:..:../,/25\/Dec\/2016 03:..:../p'
$ cat log_range.log | awk '/24\/Dec\/2016 21:..:../,/25\/Dec\/2016 03:..:../'
```

