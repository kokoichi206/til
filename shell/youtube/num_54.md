## 同じ文字が２回繰り返されるものが、ちょうど2つ現れるものを行番号とともに

```sh
$ cat oraora.txt
オラオラほげオラオラ
...

$ cat oraora.txt | grep -E '(..)\1'
$ echo "オラオラほげオラオラ" | grep -En '(..)\1.*(..)\2' | grep -Ev '(..)\1.*(..)\2.*(..)\3'
```

## 矢印が自分を向いてる方だけ選ぶ
```sh
$ cat kouun.txt
↓
運行
↑
沈降
↓
$ cat kouun.txt | tr -d \\n | grep -e '[^↓↑]*↑' -e '↓[^↓↑]*'
$ cat kouun.txt | tr -d \\n | grep -e '[^↓↑]*↑' -e '↓[^↓↑]*' 
$ cat kouun.txt | tr -d \\n | grep -o -e '[^↓↑]*↑' -e '↓[^↓↑]*'  | grep -o '[^↓↑]*'
```

pee を使う（install）

```sh
$ cat kouun.txt | pee 'grep -A1 ↓' 'grep -B1 ↑' | grep -v - | grep .. | sort -u
```

### 2文字以上を取り出す
```sh
$ grep ..
```

## あかさたな。。のどの行が何個あるか調べる
```sh
$ echo ちんすこう | uconv -x latin
chinsukou
$ echo ちんすこう | grep -o . | uconv -x latin
$ echo ちんすこう | grep -o . | uconv -x latin | sed 's/ch/t/g' | tr iueo a | grep -o ^.
$ echo ちんすこう | grep -o . | uconv -x latin | sed 's/ch/t/g' | tr iueo a | grep -o ^. | sort | uniq -c | sed 'y/akstnhmyrw/あかさたなはまやらわ/'
```

### sed yコマンド
`y/置換前リスト/置換後リスト/`

とすることで、リストの同じ位置にあるもの同士を変換できる

```sh
$ echo "$input" | sed 'y/あいうえお/アイウエオ/'
```




