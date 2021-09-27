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
```



## xargs -P の並列

### cpu の数
```bash
$ cat /proc/cpuinfo
processor       : 0
BogoMIPS        : 108.00
Features        : fp asimd evtstrm crc32 cpuid
CPU implementer : 0x41
CPU architecture: 8
CPU variant     : 0x0
CPU part        : 0xd08
CPU revision    : 3

processor       : 1
BogoMIPS        : 108.00
Features        : fp asimd evtstrm crc32 cpuid
CPU implementer : 0x41
CPU architecture: 8
CPU variant     : 0x0
CPU part        : 0xd08
CPU revision    : 3
...

$ grep processor /proc/cpuinfo 
processor       : 0
processor       : 1
processor       : 2
processor       : 3
# 論理プロセッサーの数！（並列の最大数ってここ？）
$ grep processor /proc/cpuinfo | wc -l
4
```

### 確認
並列処理されていることを確認する

```bash
$ time seq 3 | xargs -I@ sleep @
real    0m6.036s
user    0m0.001s
sys     0m0.044s

$ time seq 3 | xargs -P3 -I@ sleep @
real    0m3.025s
user    0m0.009s
sys     0m0.030s

$ time seq 3 | xargs -P4 -I@ sleep @
real    0m3.026s
user    0m0.010s
sys     0m0.030s

# 平行で走らせられる処理の数は、ここで調べられるっぽい！
$ echo $(nproc)
# その値を下のようにコマンド置換で使う
$ ls *.png | sed 's/\.png//' | xargs -P$(nproc) -I@ convert @.png @.jpg
```


## 小ネタ
```bash
# awk で三項間演算子使える
$ seq 4 | awk '{print "mkdir "($1%2 ? "odd_": "even_")$1}'
$ find shellgei160/ | grep files
# sed -n で一致したところ**のみ** print
# sed -n '/正規表現/p'
$ find . -name files.* | xargs cat | sed -n '/\.exe$/p'
$ find . -name files.* | xargs cat | awk '/\.exe$/'
```

