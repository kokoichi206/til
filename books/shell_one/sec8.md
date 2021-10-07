## ソフトウェア開発中に繰り出すワンライナー

### python のインデント確認
```sh
# match でマッチした文字の長さは、RLENGTH という組み込み変数に格納される
$ awk 'match($0, /^ +/){if (RLENGTH%4) print NR}' hoge.py
3

```

### ビットスクワッティング
発熱してビットエラーが発生しやすくなった PC は、まれに、URL を１ビット間違えることがある！？

これを利用してユーザーを偽サイトに誘導する手法を、ビットスクワッティングと呼ぶ。もし「blog.ueda.tech」の blog.ueda の部分に１ビットのビットスクワッティングが起きたら、どのような文字列になるか？

```sh
$ echo 'blog.ueda' | xxd -b -c1
00000000: 01100010  b
00000001: 01101100  l
00000002: 01101111  o
00000003: 01100111  g
00000004: 00101110  .
00000005: 01110101  u
00000006: 01100101  e
00000007: 01100100  d
00000008: 01100001  a
00000009: 00001010  .
# echo よりは、改行がない分 printf の方が良き
$ printf 'blog.ueda' | xxd -b -c1
00000000: 01100010  b
00000001: 01101100  l
00000002: 01101111  o
00000003: 01100111  g
00000004: 00101110  .
00000005: 01110101  u
00000006: 01100101  e
00000007: 01100100  d
00000008: 01100001  a
# これを横に並べると、二進数表記が得られる
$ echo 'blog.ueda' | xxd -b -c1 | awk '{printf $2}'
01100010011011000110111101100111001011100111010101100101011001000110000100001010
# 行の数だけプリントする
$ echo 'blog.ueda' | xxd -b -c1 | awk '{printf $2}' |  perl -ne '{print "$_\n" x length($_)}'
01100010011011000110111101100111001011100111010101100101011001000110000100001010
01100010011011000110111101100111001011100111010101100101011001000110000100001010
01100010011011000110111101100111001011100111010101100101011001000110000100001010
01100010011011000110111101100111001011100111010101100101011001000110000100001010
...
# 列と行が一致するところをビット反転させていく
$ echo 'blog.ueda' | xxd -b -c1 | awk '{printf $2}' |  perl -ne '{print "$_\n" x length($_)}' | awk -F '' -v OFS='' '{$NR=!$NR;print}'
11100010011011000110111101100111001011100111010101100101011001000110000100001010
00100010011011000110111101100111001011100111010101100101011001000110000100001010
01000010011011000110111101100111001011100111010101100101011001000110000100001010
01110010011011000110111101100111001011100111010101100101011001000110000100001010
01101010011011000110111101100111001011100111010101100101011001000110000100001010
01100110011011000110111101100111001011100111010101100101011001000110000100001010
01100000011011000110111101100111001011100111010101100101011001000110000100001010
...
# 解答
$ echo 'blog.ueda' | xxd -b -c1 | awk '{printf $2}' |\
  perl -ne '{print "$_\n" x length($_)}' |\
   awk -F '' -v OFS='' '{$NR=!$NR;print}' |\
    perl -nle 'print pack("B*", $_)' |\
     grep '^[a-z\.]*$' | xargs
rlog.ueda jlog.ueda flog.ueda clog.ueda bdog.ueda bhog.ueda bnog.ueda bmog.ueda blgg.ueda blkg.ueda blmg.ueda blng.ueda blow.ueda bloo.ueda bloc.ueda bloe.ueda blof.ueda blognueda blog.eeda blog.qeda blog.weda blog.teda blog.uuda blog.umda blog.uada blog.ugda blog.udda blog.ueta blog.uela blog.uefa blog.ueea blog.uedq blog.uedi blog.uede blog.uedc
```

### perl
pack

```sh
# C: unsigned char
$ perl -e 'print pack("C3", 65, 66, 67, 10)'
ABC
$ perl -e 'print pack("C3", 65, 66, 67, 10)'
ABC
```

### git
```sh
makerepo() { mkdir "$1" && cd "$1" && echo "# $1" > README.md && git init && git add README.md && git commit -m 'Initial commit'; }
# git 命令、などの「命令」を一般的に サブコマンド と呼ぶ

# 前のコミットから何時間後に次のコミットをおこなっているか
$ git log --pretty=format:%ct | sed p | sed '1d;$d' | paste - - | awk '{print ($1-$2)/3600}'
16.0831
7.20333
23.3819
4.49944
15.7158
31.845
6.46833
0.0458333
35.5994
5.88472
46.8697
19.7806

# 別解１
$ git log --pretty=format:%ct | awk 'last{print (last-$0)/3600}{last = $0}'

# 別解２
$ git log | grep ^Date:                                                      
Date:   Wed Oct 6 23:03:07 2021 +0900
Date:   Wed Oct 6 06:58:08 2021 +0900
Date:   Tue Oct 5 23:45:56 2021 +0900
Date:   Tue Oct 5 00:23:01 2021 +0900
Date:   Mon Oct 4 19:53:03 2021 +0900
...
$ git log | grep ^Date: | awk '{print $3,$4,$5,$6}' | head
Oct 6 23:03:07 2021
Oct 6 06:58:08 2021
Oct 5 23:45:56 2021
Oct 5 00:23:01 2021
Oct 4 19:53:03 2021
Oct 4 04:10:06 2021
...
$ git log | grep ^Date: | awk '{print $3,$4,$5,$6}' | head | date -f- +%s
1633561387

```



## 小ネタ
- w - Show who is logged on and what they are doing.
