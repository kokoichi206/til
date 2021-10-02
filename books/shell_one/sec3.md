## sec 3

### perl, ruby
- ruby と perl には類似性ある
- オプション
  - -n: ファイルあるいは標準入力の内容を１行ずつ読む
  - -a: １行が空白区切りで F という配列に入る
  - -l: awk のように入力から改行を除去して、出力の際に改行を入れる
  - -e: 次の引数に記述された Perl のコードを実行する  

```sh
# perl
$ echo -e "オトン オカン オカン\nオカン オトン オカン" |\
 perl -C -Mutf8 -pe 's/...$/あかん/'
オトン オカン あかん
オカン オトン あかん
# デフォルトが配列 F ? 
$ echo -e "オトン オカン オカン\nオカン オトン オカン" |\
 perl -anle '$F[2]="あかん"; print "@F"'
オトン オカン あかん
オカン オトン あかん

# ruby
## デフォルトが配列 F ? 
$ echo -e "オトン オカン オカン\nオカン オトン オカン" |\
 ruby -ane '$F[2]="あかん"; puts $F.join(" ")'
オトン オカン あかん
オカン オトン あかん
```

```sh
$ seq 3 | perl -lne 'print $_*2'
2
4
6
$ seq 3 | ruby -ne 'puts $_.to_i*2'
2
4
6
```

### python
```sh
$ seq 3 | python3 -c 'import sys; [print(2*int(a)) for a in sys.stdin]'
2
4
6
$ seq 3 | python3 -c 'import math, sys; [print(math.sqrt(int(a))) for a in sys.stdin]'
1.0
1.4142135623730951
1.7320508075688772
# なぜか、改行が入る？？ stdin の話か？
$ seq 3 | python3 -c 'import sys;[print("配列:"+a, end="") for a in sys.stdin]'
配列:1
配列:2
配列:3
```

### grep
基本正規表現（-G）、拡張正規表現（-E）、Perl正規表現（-P）

```sh
# ERE, PCRE, では、(a|b) は a or b
$ echo '(bash|nologin)' | grep -G '^(bash|nologin)$'
(bash|nologin)
# + は、ERE, PCRE では、１回以上の繰り返しを表す
$ echo C/C++ | grep -o -E C.+
C/C++
$ echo C/C++ | grep -o -G C.+   # C(何か一文字)+
C++
# \N は数字を表すという、メタ文字
$ echo 36 | grep -P '\N'
# 「と」の後ろに「まと」が続く場合に「と」だけ出力する
$ echo とまとまとまと | grep -o -P 'と(?=まと)'
## 「ルックアラウンドアサーション」という方法
## 正規表現の前後をカンニングするためのもの
$ echo とまとまとまと | grep -o -P 'と(?=まと)' | uniq -c
    3 と
$ echo 東京タワー東京ヨワー東京スカイツリー東京ヨワイツリー | perl -pe 's/東京(?!ヨ)/山本/g'
山本タワー東京ヨワー山本スカイツリー東京ヨワイツリー
```

### 大文字への変換
```sh
$ cat iampen.txt 
This is <strong>a pen</strong>. I am a pen.
<pre>Are you pen?</pre> <strong>Yes</string>, I am.

# \2 の内容を、\U で大文字にする！！！
$ sed -r 's/(<strong>)([^<]+)/\1\U\2/' iampen.txt 
This is <strong>A PEN</strong>. I am a pen.
<pre>Are you pen?</pre> <strong>YES</string>, I am.
## \L で小文字か
$ sed -r 's/(<strong>)([^<]+)/\1\L\2/' iampen.txt
## 別解
$ cat iampen.txt | perl -pe 's/(?<=<strong>)[^<]+/\U$&/'
```

### 回文チェック
```sh
# 「-f -」、標準入力（-）から正規表現のリストを読み込む
# -x:　行全体が正規表現とマッチしないとマッチしたことにならない
$ rev kaibun.txt | grep -xf - kaibun.txt

$ cat kaibun.txt | ruby -lne 'puts $_ if $_==$_.reverse'
$ echo 'トマト' | ruby -lne 'puts $_ if $_==$_.reverse'
トマト
$ paste kaibun.txt <(rev kaibun.txt) | awk '$1==$2{print $1}'

# えぐい
$ paste <(grep -o . not_kaibun) <(grep -o . not_kaibun | tac) | awk '$1!=$2'
$ diff <(grep -o .kaibun) <(grep -o . kaibun | tac) | awk '$1!=$2'
```

### 括弧の対をチェック
```sh
$ echo '((し)))(((ok)))((ん))(((out)((これもだめ)))(((((ゆるそう)))))' |\
 sed 's@)(@)\n(@g'
((し)))
(((ok)))
((ん))
(((out)
((これもだめ)))
(((((ゆるそう)))))
# PCRE, \g<数字>：部分式呼び出し
## grep -P '^(\(\g<1>\)|[^()]+)$':
## 
$ echo '((し)))(((ok)))((ん))(((out)((これもだめ)))(((((ゆるそう)))))' |\
 sed 's@)(@)\n(@g' | grep -P '^(\(\g<1>\)|[^()]+)$'
(((ok)))
((ん))
(((((ゆるそう)))))
# paste -s: -s で読み込んだ各行を横に並べる
## -d '' で並べる時の区切り文字を空文字にしている
$ echo '((し)))(((ok)))((ん))(((out)((これもだめ)))(((((ゆるそう)))))' |\
 sed 's@)(@)\n(@g' | grep -P '^(\(\g<1>\)|[^()]+)$' |\
  tr -d '()' | paste - -sd ''
okんゆるそう
```

### sed のラベル
- sed ':a; s/xxx/YYY/g; ta', a~ta -> a に戻るを繰り返す（成功したら）

```sh
$ echo '(((((hoge))))))' | sed 's/\(([^)]+)\)/\1/g'
(((((hoge))))))
# ん？ sed の中って、逆にエスケープする必要がある？（メタ文字とかだけ？）
$ echo '(((((hoge))))))' | sed "s/(\([^)]\+\))/\1/g"
((((hoge)))))
# ラベル使うぞ！
## a のラベル、a~ta の繰り返し
$ echo '(((((hoge))))))' | sed ":a; s/(\([^)]\+\))/\1/g ;ta"
hoge)
# sed '/正規表現/d' は、マッチしたら消す
$ echo '(((((hoge))))))' | sed ":a; s/(\([^)]\+\))/\1/g ;ta; /[()]/d"
$ echo '((((((hoge))))))' | sed ":a; s/(\([^)]\+\))/\1/g ;ta; /[()]/d"
hoge
```

### format
```sh
$ echo -e '# 見出し\n\n本文です。\n\n* 箇条書きです。\n* これも箇条書き。'
# 見出し

本文です。

* 箇条書きです。
* これも箇条書き。

$ echo -e '# 見出し\n\n本文です。\n\n* 箇条書きです。\n* これも箇条書き。' | pandoc
<h1 id="見出し">見出し</h1>
<p>本文です。</p>
<ul>
<li>箇条書きです。</li>
<li>これも箇条書き。</li>
</ul>
# pandoc -s だとヘッダなどもつけてくれる
$ echo -e '# 見出し\n\n本文です。\n\n* 箇条書きです。\n* これも箇条書き。' | pandoc -s
```

### 重複
```sh
$ echo hogehoge | grep -oE '(.+)\1'
hogehoge
$ cat diarydiary.txt | tr -d '\n' | grep -oE '(.+)\1'
```

### 改行
```sh
# s は空行で折り返すためのオプション
$ cat hogehoge.txt | fold -s -w 31 | sed '/ *$//'
# 以下のようにすると文字が切れないように、指定文字以内で改行できる
$ cat hogehoge.txt | sed 's/ /\n/g; s/$/ /' |\
 awk '{L+=length}L > 31 {print ""; L=length}{printf $0}'
$ cat hogehoge.txt | sed 's/ /\n/g; s/$/ /' |\
 awk '{L+=length}L > 31 {print ""; L=length}{printf $0}'|\
 awk 'sub(/ $/,"")'
```

```sh
# -r は require を行なっている
$ echo -e "私が小学校一年生の時は\n、四七都道府県の位置" |\
 ruby -rzen_to_i -ne 'puts $_.zen_to_i'
私が小学校1年生の時は
、47都道府県の位置
# sed -z オプション
## -z, --null-data : separate lines by NUL characters
## 勝手に改行は入んないっぽい＋行ごとに取り扱うのをやめてるな
$ echo -e "私が小学校一年生の時は\n、四七都道府県の位置" |\
 ruby -rzen_to_i -ne 'puts $_.zen_to_i' | sed -z 's/\n[、。]//g'
私が小学校1年生の時は47都道府県の位置
$ echo -e "私が小学校一年生の時は\n、四七都道府県の位置" |\
 ruby -rzen_to_i -ne 'puts $_.zen_to_i' | sed -zE 's/\n([、。])/\1\n/g'
私が小学校1年生の時は、
47都道府県の位置

## uniq -f1 -u, -f1:一列目を無視して比較、-u: ひとつしかないレコードを出力
```

### 順序付きリストの整形
markdown のリストの数字が、1.,1.,1. などとなっていたら、その数字を正しくアップさせていく

```sh
# # が先頭に来るたびに数値をリセット
$ cat item.md | awk '/^[0-9]\./{a++; $1=a"."; print}/^#/{a=0}!/^[0-9]\./'
```




## 小ネタ
- *? で最短一致になる
- paste fileA fileB
- grep -P の先読み機能
- awk で、パターンに処理を書いてしまうてもある...
- awk, sub(置換前, 置換後), で置換する
  - gsub(置換前, 置換後) はとにかく置換を試みて、できた数を返す
- sed のラベル
  - sed ':a; s/xxx/YYY/g; ta', a~ta -> a に戻るを繰り返す（成功したら）
- 安定ソートをかけるには、`sort -s`
- 改行を無視して検索する
  - sed -s
