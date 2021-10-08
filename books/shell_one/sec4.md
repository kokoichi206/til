## sec 4 データの管理、集計、変換

### 四捨五入の巻
```sh
# 少数第２桁で四捨五入
## awk
$ cat table.txt | awk '{print $0,$2+$3}' | awk '{print $0, int(($4 + ($4>0?0.05:0-.05))*10)/10}'
## ruby
$ cat table.txt | awk '{print $0,$2+$3}' | ruby -ane '$F[4]=$F[3].to_f.round(1); puts $F.join(" ")'
## python
### あんまりワンライナーで四捨五入に向かない
```

### join
```sh
$ cat master.txt 
01 みかん
02 バナナ
03 リンゴ
$ cat transaction.txt 
01 4
01 3
02 9
04 3
# join は１列目のデータをキーとして２つのファイルを連結する！！
$ join master.txt transaction.txt 
01 みかん 4
01 みかん 3
02 バナナ 9
```

### ps
```sh
# ユーザーごとの CPU 使用率の集計
$ ps aux | awk 'NR>1{p[$1] += $3; n[$1]++}END{for(i in p) print p[i], n[i], i}'
0 3 systemd+
166.8 112 ubuntu
0 1 whoopsie
0 1 message+
0 7 postgres
0 2 kernoops
0 1 syslog
0 1 colord
0 1 rtkit
0 9 www-data
0 2 avahi
0 3 proxy
0 3 postfix
0.1 1 mysql
0 1 daemon
1.6 174 root

$ ps aux | awk 'NR>1{p[$1] += $3; n[$1]++}END{for(i in p) print p[i], n[i], i}' | sort -nrk 1,2
```

### 売り上げの集計
```sh
# 商品番号 枝番 商品名 価格
$ cat stones_master 
001 01 シェル石 300
001 02 シェル石（お詫び用） 0
002 01 非行石（青） 1000
002 02 非行石（偽物・赤） 10
004 01 おじいちゃんから出た石 1
005 01 デーモンコア 100000
005 02 デーモンコア（お詫び用） 0
$ cat sales 
20180822 101212 003 01 5
20180822 101212 001 01 3
20180822 101213 002 01 10
20180822 101214 004 01 8
20180822 101215 005 01 2
20180822 101215 001 01 2
20180822 101215 002 02 7
20180822 101216 004 01 23
20180822 101216 001 03 9

# 商品番号と枝番を連結したものをキーにする
$ awk '{a[$3$4]+=$5}END{for(k in a)print k, a[k]}' sales | sort
00101 5
00103 9
00201 10
00202 7
00301 5
00401 31
00501 2
# 最終形
$ awk '{a[$3$4]+=$5}END{for(k in a)print k, a[k]}' sales | sort | join <(sed 's/ //' stones_master) - | awk '{print $2, $3*$4}'
シェル石 1500
非行石（青） 10000
非行石（偽物・赤） 70
おじいちゃんから出た石 31
デーモンコア 200000
```

### No.51
```sh
$ cat scores.txt | awk '{$1=sprintf("%03d", $1); print}'
006 95
002 40
005 80
008 76
# 名前のデータは絶対含めつつ（行が存在しなくても表示）連結
$ cat scores.txt | awk '{$1=sprintf("%03d", $1); print}' | sort | join -a 1 students.txt -
001 井田
002 上田 40
003 江田
004 織田
005 加田 80
# 点数が存在しない部分は、０点として扱う
$ cat scores.txt | awk '{$1=sprintf("%03d", $1); print}' | sort | join -a 1 students.txt - | awk 'NF==2{print $0,0}NF==3'
001 井田 0
002 上田 40
003 江田 0
004 織田 0
005 加田 80
```

### クロス集計
```sh
$ awk 'FNR==1 {$1=""; h=$0}FNR!=1{print $0,h}' data_U
X 4 2  A B
Y 3 1  A B
# FILENAME, 列の数を表示する
$ awk 'FNR==1 {$1=""; h=$0}FNR!=1{print FILENAME,$0,h,NF-1}' data_U data_V
data_U X 4 2  A B 2
data_U Y 3 1  A B 2
data_V X 7 6 -1  A B C 3
data_V Y 9 8 -2  A B C 3
# 各行から、列の数だけ出力が増える
$ awk 'FNR==1 {$1=""; h=$0}FNR!=1{print FILENAME,$0,h,NF-1}' data_U data_V | awk '{for(i=NF-$NF; i<NF; i++)print $1,$2,$i,$(i-$NF)}'
data_U X A 4
data_U X B 2
data_U Y A 3
data_U Y B 1
data_V X A 7
data_V X B 6
data_V X C -1
data_V Y A 9
data_V Y B 8
data_V Y C -2
# ファイル名、行、列、値
$ awk 'FNR==1 {$1=""; h=$0}FNR!=1{print FILENAME,$0,h,NF-1}' data_U data_V | awk '{for(i=NF-$NF; i<NF; i++)print $1,$2,$i,$(i-$NF)}' | sed 's/data_//'
U X A 4
U X B 2
U Y A 3
U Y B 1
V X A 7
V X B 6
V X C -1
V Y A 9
V Y B 8
V Y C -2
```

### No 53 欠損値の補完
```sh
# join の output の並ばせ方の指定： -o
# 空欄値の処理： -e (o と一緒に指定しないと効かない？)
$ cat devicelist.txt | awk '{print $2, $1}' | sort | join -a 1 -a 2 -o 1.2 0 2.2 -e @ - <(cat measurement.txt | sort)
07 xxxx.0a69.b711 3119
06 xxxx.0c4d.095c 3235
01 xxxx.0c4d.1c45 1914
03 xxxx.0d17.73a6 2275
10 xxxx.0d17.7478 3443
05 xxxx.0d17.9658 @
02 xxxx.0d46.f3c2 @
08 xxxx.0d81.1da2 @
@ xxxx.0d81.33a8 1607
04 xxxx.0d81.33b8 @
...
```

### jq
```sh
$ cat article.json  | jq .year.start
2017
$ cat article.json  | jq .year.starte
null
```

### u
```sh
# 2,$p で、２秒目から末尾までの行をデフォルト出力＋もう一度出力、
# $d で末尾の行を削除
$ seq 4 | sed '2,$p;$d'
1
2
2
3
3
4
# paste -d, で delimiter を指定
$ seq 4 | sed '2,$p;$d' | paste -d , - -
1,2
2,3
3,4
$ seq 4 | sed '2,$p;$d' | paste -d , - - | sed 's/.*/[&]/'
[1,2]
[2,3]
[3,4]
```

### No.57
```sh
$ cat table.md 
|AAA|BBB|CCC|
|---|---|---|
|1|123|4|
|10000|1|64|
|3|3|3|
# column -t を使う
$ cat table.md | sed 's/|/ & /g' | column -t
|  AAA    |  BBB  |  CCC  |
|  ---    |  ---  |  ---  |
|  1      |  123  |  4    |
|  10000  |  1    |  64   |
|  3      |  3    |  3    |
# 余計な空行は
$ cat table.md | sed 's/|/ & /g' | column -t | sed 's/ |/|/g; s/| /|/g'
| AAA   | BBB | CCC |
| ---   | --- | --- |
| 1     | 123 | 4   |
| 10000 | 1   | 64  |
| 3     | 3   | 3   |
```

pandoc を使う

```sh
$ cat table.md | pandoc -t gfm
| AAA   | BBB | CCC |
| ----- | --- | --- |
| 1     | 123 | 4   |
| 10000 | 1   | 64  |
| 3     | 3   | 3   |
```

cat で空行に空白があるか

```sh
$ cat -ET table.md 
|AAA|BBB|CCC|$
|---|---|---|$
|1|123|4|$
|10000|1|64|$
|3|3|3|$
# タブの見える化
$ cat table.md | sed 's/^/\t/g' | cat -ET
^I|AAA|BBB|CCC|$
^I|---|---|---|$
^I|1|123|4|$
^I|10000|1|64|$
^I|3|3|3|$
```

### CSV ファイルの数字の集計（ダブルクォート）
1,234 とかの、, と、コンマが被ることが問題になったりする！！！

```sh
$ cat num.csv 
1,2.3,3.99999999999999999999999
"1,234,567",789, 8,-9,"-0.1"
# xargs は "" で囲まれてところを１つの引数として解釈する
$ cat num.csv | tr ',' ' ' | xargs -n 1 
1
2.3
3.99999999999999999999999
1 234 567
789
8
-9
-0.1
# ここまでがきも！
$ cat num.csv | tr ',' ' ' | xargs -n 1 | tr -d ' ' | xargs | tr ' ' + | bc
1235362.19999999999999999999999
```

### date コマンド
```sh
# -d オプションで、今日や任意の日付から数日前、数日後の日付を出力
$ date -d '1 day ago'
Thu Oct  7 12:59:48 UTC 2021
$ date -d '1 day' +%Y%m%d
20211009
$ date -d '100 day' +%Y%m%d
20220116
$ date -d '1 month ago'
Wed Sep  8 13:21:31 UTC 2021
```

### Dateutils
Dateutils コマンドを覚えると、date よりも自在な出力が得られる。

特に日付の差の計算や日付を列挙する機能は date にはなく、便利

```sh
$ sudo apt install dateutils
$ dateutils.ddiff 2020-01-01 2020-01-03
2
$ dateutils.dadd 2020-01-01 2
2020-01-03
$ echo 2020-01-01 00:00:00 | dateutils.dconv --zone America/New_York
2019-12-31T19:00:00
# 直後の日曜日を求める
$ dateutils.dround 2020-08-14 +Sun
2020-08-16
# 直後の日曜日を求める
$ dateutils.dround 2020-08-14 -- -Sun
2020-08-09
```

### プレミアムフライデー
月末の金曜日を出力する

```sh
# uniq -w7: 各行7文字目までを調査し、前行と異なる場合だけ出力する
$ seq 0 365 | xargs -I@ date '+%F %a' -d '2021-01-01 @day' |\
 grep 'Fri' | tac | uniq -w7 | tac
2021-01-29 Fri
2021-02-26 Fri
2021-03-26 Fri
2021-04-30 Fri
2021-05-28 Fri
2021-06-25 Fri
2021-07-30 Fri
2021-08-27 Fri
2021-09-24 Fri
2021-10-29 Fri
2021-11-26 Fri
2021-12-31 Fri

# 別解
$ printf '2021-%02d-01\n' {1..12}
2021-01-01
2021-02-01
2021-03-01
2021-04-01
2021-05-01
2021-06-01
2021-07-01
2021-08-01
2021-09-01
2021-10-01
2021-11-01
2021-12-01
# 31 を足して来月まで進めた後、直前の金曜日まで戻す
$ printf '2021-%02d-01\n' {1..12} | dateutils.dround -- +31d -Fri
2021-01-29
2021-02-26
2021-03-26
2021-04-30
2021-05-28
2021-06-25
2021-07-30
2021-08-27
2021-09-24
2021-10-29
2021-11-26
2021-12-31
```

### 日付を条件にファイルを検索する
```sh
8$ seq -f "$(date +%F) %g hour" 0 -1 -400 | head
2021-10-08 0 hour
2021-10-08 -1 hour
2021-10-08 -2 hour
2021-10-08 -3 hour
2021-10-08 -4 hour
2021-10-08 -5 hour
2021-10-08 -6 hour
2021-10-08 -7 hour
2021-10-08 -8 hour
2021-10-08 -9 hour
# へーこうやって後から %Y とかを指定することもできるんだ
$ seq -f "$(date +%F) %g hour" 0 -1 -400 | date -f - '+touch -t %Y%m%d%H%M %F_%T' | head
touch -t 202110080000 2021-10-08_00:00:00
touch -t 202110072300 2021-10-07_23:00:00
touch -t 202110072200 2021-10-07_22:00:00
touch -t 202110072100 2021-10-07_21:00:00
touch -t 202110072000 2021-10-07_20:00:00
touch -t 202110071900 2021-10-07_19:00:00
touch -t 202110071800 2021-10-07_18:00:00
touch -t 202110071700 2021-10-07_17:00:00
touch -t 202110071600 2021-10-07_16:00:00
touch -t 202110071500 2021-10-07_15:00:00
```

### find
```sh
$ seq -f "$(date +%F) %g hour" 0 -1 -400 | date -f - '+touch -t %Y%m%d%H%M %F_%T' | sh
$ find . -daystart -mtime -$((8 + $(date '+%w'))) -mtime +$(date '+%w') -type f | sort
```

### ５回日曜日がある月は？
```sh
# date -f - は、変換対象のレコードを標準入力から読み込む
# 日曜日 0 ちゃうんかな
$ seq 0 364 | sed 's/^/20210101 /' | sed 's/$/ days/' |\
 date -f - '+%m %w' | head
01 5
01 6
01 0
01 1
01 2
01 3
01 4
01 5
...

$ seq 0 364 | sed 's/^/20210101 /' | sed 's/$/ days/' |\
 date -f - '+%m %w' | grep 0$ | uniq -c
      5 01 0
      4 02 0
      4 03 0
      4 04 0
      5 05 0
      4 06 0
      4 07 0
      5 08 0
      4 09 0
      5 10 0
      4 11 0
      4 12 0
$ seq 0 364 | sed 's/^/20210101 /' | sed 's/$/ days/' |\
 date -f - '+%m %w' | grep 0$ | uniq -c | awk '$1 == 5{print $2}'
01
05
08
10
$ seq 1 12 | xargs -I@ ncal @ 2021 |\
 grep -B1 -E '^Su *( +[0-9]+){5}' | grep 2021 | tr -d ' 2021'
January
May
August
October
```

### 時間の限界
普通にこれ、すごい！

```sh
$ f=0; t=$(bc <<< 2^100); while [ $(bc <<< $t-$f) != 1 ]; do m=$(bc <<< "($f+$t)/2"); echo $m; date -d @$m && f=$m || t=$m; done
```




## 小ネタ
- `$ for i in $(cd /usr; echo *); do echo $i; done`
- フォーマット指定子 (format specifier)
  - %c, %8s, %-10s, 
  - 整数: %-2d, %03d, %2u, %02u, %06u, %04x,
  - %5.2f, %5.3e, %g (実数を最適な形で)
  - %g ⇦ 005 が 5 になった
- awk 内でファイル名： FILENAME
- jq で、各キーの値にアクセスする方法
  - cat article.json  | jq .year.starte
- xargs は "" で囲まれてところを１つの引数として解釈する
- `info date`
- date -d @Unix時間

```sh
$ f=0; t=$(bc <<< 2^100); while [ $(bc <<< $t-$f) != 1 ]; do m=$(bc <<< "($f+$t)/2"); echo $m; date -d @$m && f=$m || t=$m; done
```
