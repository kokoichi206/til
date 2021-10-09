## sec 5 文字コードとバイナリ
nkf, iconv

### n 進数
```sh
# printf 16 進数
$ printf "%x\n" 17
11
# 元の基数に戻すには、Bash の算術展開を利用
$ echo $(( 16#11 ))
17
$ echo $(( 2#11 ))
3
$ a=111
$ echo $(( 2#$a ))
7

$ echo 33 | ruby -ne 'a=$_.to_i; puts a.to_s(16), a.to_s(8), a.to_s(2)'
21
41
100001
```

### ASCII
```sh
$ ascii
Usage: ascii [-adxohv] [-t] [char-alias...]
   -t = one-line output  -a = vertical format
   -d = Decimal table  -o = octal table  -x = hex table  -b binary table
   -h = This help screen -v = version information
Prints all aliases of an ASCII character. Args may be chars, C \-escapes,
English names, ^-escapes, ASCII mnemonics, or numerics in decimal/octal/hex.

Dec Hex    Dec Hex    Dec Hex  Dec Hex  Dec Hex  Dec Hex   Dec Hex   Dec Hex  
  0 00 NUL  16 10 DLE  32 20    48 30 0  64 40 @  80 50 P   96 60 `  112 70 p
  1 01 SOH  17 11 DC1  33 21 !  49 31 1  65 41 A  81 51 Q   97 61 a  113 71 q
  2 02 STX  18 12 DC2  34 22 "  50 32 2  66 42 B  82 52 R   98 62 b  114 72 r
  3 03 ETX  19 13 DC3  35 23 #  51 33 3  67 43 C  83 53 S   99 63 c  115 73 s
...
```  

```sh
# sed の i コマンド
$ ascii | grep ' [X-Z] ' | awk '{print $16}' | sed 1iobase=2
obase=2
88
89
90
$ ascii | grep ' [X-Z] ' | awk '{print $16}' | sed 1iobase=2 | bc
1011000
1011001
1011010

$ ascii | grep ' [X-Z] ' | awk '{print $16}' | sed 1iobase=2 | bc
1011000
1011001
1011010
$ ascii | grep ' [X-Z] ' | awk '{print $16}' | sed 1iobase=2 | bc |\
 sed 's/^/0/' | paste -s 
01011000        01011001        01011010
# paste: -s, --serial
#  paste one file at a time instead of in parallel
$ ascii | grep ' [X-Z] ' | awk '{print $16}' | sed 1iobase=2 | bc |\
 sed 's/^/0/' | paste -sd ''
010110000101100101011010
```

### Unicode と utf-8 の関係？
```sh
# unicode と UTF-8 で数字が異なる
## U+5A9B, 0xE5AA9B
$ echo -e '\U5A9B' '\xE5\xAA\x9B'
媛 媛
$ echo -e '\U5A' '\x5A'
Z Z

$ echo 5A 5A9B E5AA9B | xargs -n 1 | sed '1iibase=16; obase=2' |\
 bc | xargs printf "%24s\n" 
                 1011010
         101101010011011
111001011010101010011011
$ echo 5A 5A9B E5AA9B | xargs -n 1 | sed '1iibase=16; obase=2' |\
 bc | xargs printf "%24s\n" | sed -r 's/.{8}/& /g'
                   1011010 
          1011010 10011011  # １バイト目が、ASCII の Z と区別できない
11100101 10101010 10011011 
# UTF-8 の符号化方式
## 11100101 の 1110 は、「３バイトで１文字である」ということを示している。
## 後半２バイトの先頭の 10 は、これらが先頭の１バイトではないことを示している。
## UTF-8 ではこのように、先頭を見ることで ASCII か それ以外かを見分けている

## UTF-8, 1文字に当てるデータの長さが可変
## 一方、Unicode の符号化方式には UTF-16 や UTF-32 が存在し、これらは固定帳。
## Unicode は固定長であるが故に、ASCII と被りのバイトが出てしまう。
## tr コマンドなどで、長さが変わって変なことになってしまう。

# uniname
## 0x0A: Fine Feed
$ echo 媛 | LINES=10 uniname
character  byte       UTF-32   encoded as     glyph   name
        0          0  005A9B   E5 AA 9B       媛      CJK character Nelson 1238
        1          3  00000A   0A                     LINE FEED (LF)
```

### nkf
Shift_JIS

```sh
$ cat shift_jis.txt 
���̕��͂̓V�t�gJIS��
������Ă��܂��B
��ļ޽!!
# -Lu は、CRLF をラインフィード（LF）だけに変換する
# -w は、テキストを UTF-8 に変えるオプション
$ nkf -wLu shift_jis.txt 
この文章はシフトJISで
書かれています。
シフトジス!!
# -x は、カタカナが半角になるのを防止する
## nkf -wLux が、Windows 用から Linux 用に
## テキストファイルを変換するときの標準的な nkf の用法
$ nkf -wLux shift_jis.txt 
この文章はシフトJISで
書かれています。
ｼﾌﾄｼﾞｽ!!
## 逆に、Linux から Windows 用にテキストファイルを変換する時
### -s が　Shift_JIS への変換
### -Lw が LF から CRLF への変換
$ echo 吾輩は猫である。 | nkf -sLwx
��y�͔L�ł���B
$ echo 吾輩は猫である。 | nkf -sLwx | nkf -wLux
吾輩は猫である。

$ nkf shift_jis.txt | xxd -p
e38193e381aee69687e7aba0e381afe382b7e38395e383884a4953e381a7
0d0ae69bb8e3818be3828ce381a6e38184e381bee38199e380820d0ae382
b7e38395e38388e382b8e382b921210d0a
# 0x0d は carriage return, windows では CRLF
$ diff <(nkf shift_jis.txt | xxd -p | fold -b2) <(nkf -wLu shift_jis.txt | xxd -p | fold -b2)
31d30
< 0d
57d55
< 0d
76d73
< 0d
```

### iconv
iconv

-f : from

-t : to

```sh
$ cat shift_jis.txt | iconv -f SHIFT_JIS -t UTF-8
この文章はシフトJISで
書かれています。
ｼﾌﾄｼﾞｽ!!
# 注：改行コードは変換してくれない
$ cat shift_jis.txt | iconv -f SHIFT_JIS -t UTF-8 | xxd -p | grep -o 0d0a
0d0a
0d0a
0d0a
$ cat shift_jis.txt | iconv -f SHIFT_JIS -t UTF-8 | tr -d '\r' |\
 xxd -p | grep -o 0d0a
```

### 文字のバイト数の調査
```sh
$ cat uni.txt | grep -o . |\
 while read s; do echo -n $s" "; echo -n $s | wc -c; done
a 1
± 2
運 3
🎂 4
```

### バイナリを操る
BOM (byte order mark): 上の桁から並べるか、下の桁から並べるか

```sh
$ file game
game: ELF 64-bit ...
# ELF: Executable and Linking Format
## 何かのプログラムで、コマンドとして実行できる

# Base64 はエンコード方式の１つ
$ base64 game
f0VMRgIBAQAAAAAAAAAAAAMAPgABAAAA4BEAAAAAAABAAAAAAAAAAAA/AAAAAAAAAAAAAEAAOAAN
AEAAIAAfAAYAAAAEAAAAQAAAAAAAAABAAAAAAAAAAEAAAAAAAAAA2AIAAAAAAADYAgAAAAAAAAgA
AAAAAAAAAwAAAAQAAAAYAwAAAAAAABgDAAAAAAAAGAMAAAAAAAAcAAAAAAAAABwAAAAAAAAAAQAA
...
# = は、データを４の倍数にするためのパディング
$ echo hoge | base64
aG9nZQo=
# -d でデコード
$ echo 'aG9nZQo=' | base64 -d
hoge

# データが欠損してないかの確認などに使う
$ md5sum game* white*
b106ffb345374eb485d765cfb7679e48  game
99de2ae3e9798444a2e1ba80e7403707  game.cpp.gz
6a3a60dbe323767606eb5c75936d167c  white_negi.jpg
```

### 2進数から文字列を復元
```sh
# obase が先、ibase が後
## ibase を先に書くと、obase=16 の 16 が2進数として解釈されていまう
$ cat zeroone | sed '1iibase=2;obase=16' | bc
120211110210212221211020012211010101220212222022120212221001111110
$ cat zeroone | sed '1iobase=16;ibase=2' | bc
E4B88DE58AB4E68980E5BE970A
# xxd -p -r: 16 真数を羅列したテキストを読んでデコードする
$ cat zeroone | sed '1iobase=16;ibase=2' | bc | xxd -p -r
不労所得
```

### No.81, BOM の識別
```sh
$ cat bom.txt 
ボムボムプリンおいしい
# 「efbbbf」が BOM の3バイト
$ cat bom.txt | xxd -p
efbbbfe3839ce383a0e3839ce383a0e38397e383aae383b3e3818ae38184
e38197e381840a
$ cat bom.txt | xxd -p | sed "s/^efbbbf/$(echo -n '[BOM]' |\
 xxd -p)/" | xxd -p -r
[BOM]ボムボムプリンおいしい
```

### No.84. 改行コードの識別と集計
```sh
$ zcat newline.txt.gz | tr -dc '\015\012' | sed -z 's/\x0d/CR/g; s/\x0a/LF&/g' | sort | uniq -c | awk '{print $2,$1}'
CRLF 8
LF 8
```

### No.89
ファイルの最後が==で埋められているので、これは Base64 でエンコードされたデータかな？と予想できる

```sh
$ base64 -d ctf-data > a
$ file a
a: gzip compressed data, last modified: Wed Jan  1 02:45:10 2020,
from Unix, original size modulo 2^32 8296

$ base64 -d ctf-data | zcat > a
$ file a
a: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked,
interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0,
BuildID[sha1]=58c679d345acbfa866d64d36ce12cbe5dc5fd7f4, not stripped

# EFL ファイルは邪悪なプログラムの可能性があるので、実行は気をつける

# ASCII コードで、! は # の2文字前なので、以下の tr で、2文字ずつずらせる
$ echo abcde | tr '#-z' '!-z'
_`abc

```



### Memo 置き場
```sh
$ printf "%04o\n" 11
0013
$ echo "obase=2; 3" | bc
11

# 1i, a
$ echo 'hoge' | sed -e 1ibegin -e aafter
begin
hoge
after

$ echo -e "\x45"

# １行目から３行ごとに出力
$ sed -n '1~3p'
```

### 小ネタ
- printf 
  - 16 進数： %x, 8 進数： %o
- sed -e 1i文字列 -e a文字列 
  - sed 1ipien
    - １行目の前に、文字列を挿入
- ワンライナーにとっては、xxd -p の出力が一番使いやすい
- 複合コマンド「(())」: 
  - 展開をせずに、代わりに計算結果に応じて終了ステータスを返す。
- ダメ文字
  - 0x5c: 5C問題
- tr: 8進数、sed: 16進数
  - tr -dc '\015\012'

