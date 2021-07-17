# book?
なんの本か忘れた

## sed
```
echo {a..e} | xargs -n 1 | sed '/b/,/d/s/./???/'
echo {a..e} | xargs -n 1 | sed -n '2,4p'
```

## awk

### GNU Awk のインストール
```
which awk
ls -l /usr/bin/awk
sudo yum install gawk
```

### 文字数を数える
```
cat memo.md | sed 's/./&\n/g' | awk 'NF!=0' | wc -l
cat memo.md | sed 's/./&\n/g' | awk 'NF!=0' | sort | uniq -c | sort
```


## ~ などの文字をうまく入力する
- Unicodeを使いたおす。

```
echo -e U+007E '\u007E'
echo -e U+02DC '\u02DC'
```

## 全角文字のあとに、半角ピリオドなどが来てないかチェックする.
- 文字コードに明るいといろいろな調査ができる。

```
cat memo.md | grep -o '.[.。]'
```

- 全角文字が 3 バイト、半角が 1バイトであることを利用する

```
cat memo.md | grep -o '.[.。]' | LANG=C awk '{print length($1)}'
cat memo.md | grep -o '.[.。]' | LANG=C awk 'length($0)==4'
```

- 元のファイルとチェック

```
cat memo.md | grep -o '.[.。]' | LANG=C awk 'length($0)==4' | sort -u > tmp.list
cat memo.md | grep -F -f tmp.list
```

- grep -F: 正規表現を使わないときの言葉

### Unicode にする
```
od -x memo.md
```

## Shift-JISのようなWinの改行コード
- LF: 0x0a
    - これはUNIXにも存在する.
- CR: 0x0d

- LF+CR: 0a0d

### 0x0dが存在するかだけをチェックする
```
cat memo.md | od -x | grep 0d
```

### キストの表記上必要のないバイナリの削除
- DBや特殊な計算機から入手した場合、変なバイナリがあるときも

- 0x00-0xffまでバイナリを全部出力
```
awk 'BEGIN{for(i=0;i<256;i++){printf("%c",i)}}' > asc > ascii
wc -c ascii
```
なんで最初の wc -c ascii が256じゃない？
ここから可読可能なもののみを残す
```
cat ascii | tr -dc "[:print:]\n\t"
```
- [:print:] -> 文字クラスで、「印字できる字」という意味

### iconv
```
cat ascii | iconv -c -f ASCII -t ASCII | od -t x1
```
- これで変なバイナリは削除される
- 0x80 以上が消えている

```
echo -e 'こん\xffにちは'
echo -e 'こん\xffにちは' | iconv -f UTF-8 -t UTF-8
```

### nkf
- 半角カタカナを全角カタカナへ
    - 数字は半角の方がよい
    - うまくやるには、-Z0

```
echo ｶﾞｷﾞｸﾞｹﾞｺﾞ | nkf
echo オジｻﾝの電話番号１２３ー４５６７ | nkf -Z0
```

### 20文字ごとで改行
```
cat memo.md | tr -d '\s\n' | sed 's/.\{20\}/&\n/g'
```


## 特殊なデータを扱う

```
echo -e 'あいうえお\nかきくけこ' | nkf -sLwx > shift_jis.txt
nkf -g shift_jis.txt
od shift_jis.txt
```

なぜかodは8進数
```
od -x shift_jis.txt
```

xxd など、いろいろ遊ぶ
```
cat shift_jis.txt | xxd -p | fold -b4 | sed 's/82a2/82ee/' > tmp
cat tmp | xxd -r -p | nkf -g
cat tmp | xxd -r -p | nkf
```

## インターネットとの付き合い方

### Web API
```
curl http://zip.cgis.biz/csv/zip.php?zn=1130001 2> /dev/null | nkf -wLu
curl http://zip.cgis.biz/xml/zip.php?zn=1130001 2> /dev/null | nkf -wLu
curl http://zip.cgis.biz/xml/zip.php?zn=1130001 2> /dev/null | nkf -wLu | grep '<value' | grep -o '[^ ]*="[^"]*"' | sed 's;="; ;'
```

- @ubuntu
```
sudo apt-get install html-xml-utils
```
からの〜〜
```
curl http://zip.cgis.biz/xml/zip.php?zn=1130001 2> /dev/null | nkf -wLu | hxselect value -s '\n' | grep -o '[^ ]*="[^"]*"' | sed 's;="; ;'
```

### 自分のGitのすべてのリポジトリをダウンロード
```
curl `curl https://api.github.com/users/kokoichi206 | jq .repos_url -r` | jq '.[].clone_url' -r | xargs -I@ git clone @
```
jq は単なるJSON整形ツールではなく、実はいろいろできる

### 自分のサイトがごっそりダウンロードできた....
```
wget -r http://koko-django-website.herokuapp.com
```

#### 写真一覧を相対パスで取得したい
```
ls -R | grep .png | xargs -I@ find . -name @
```

#### リストの中身のみを取り出したい
```
cat index.html | grep "li>" | tr -d ' ' | sed 's;<[^<]*>;;g'
```

#### 特定の id, class 名を持つ範囲のみ取り出したい
```
sed -n '/class="box bg-gray"/,/<\/div>/p' index.html
```

#### id のかぶりがないかチェックしたい
```
cat index.html | grep -o 'id="[^"]*"' | sort | uniq -d
```


## MeCab
- [オープンソース 形態素解析エンジン](https://taku910.github.io/mecab/)
 
