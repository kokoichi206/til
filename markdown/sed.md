# sed 豆知識

最近知った sed の便利な機能を紹介していきます！

[目次]

[:contents]

## sed -n '/正規表現/p'

正規表現を含む行を抜き出します。grep みたいな使い方ですね

```sh
$ echo -e "my number is 9 digit\n090-893-893" |\
 sed -n '/[0-9]\{3\}-[0-9]\{3\}-[0-9]\{3\}/p'
090-893-893
```

## sed -n '/正規表現1/,/正規表現2/p'

正規表現1 にマッチする行から、正規表現2 にマッチする行までを出力します。

注意としては下の例のように、マッチする部分があった瞬間に出力をやめることです（c1 で終わることに注意）。

```sh
$ echo {a..c}{1..5} | xargs -n 1 | sed -n '/b[0-9]/,/c[0-9]/p'
b1
b2
b3
b4
b5
c1
```

## 続けて条件を指定できる

シェルで ";" をで行を区切って記述を続けられるように、sed の中でも ";" が使えます。

```sh
$ echo '私はあほだ' | sed 's/私/あなた/g'
あなたはあほだ
$ echo '私はあほだ' | sed 's/私/あなた/g; s/あほ/天才/g'
あなたは天才だ

# 上の例は以下と等価
## パフォーマンス的にどっちがいいかとかは分からない
$ echo '私はあほだ' | sed 's/私/あなた/g' | sed 's/あほ/天才/g'
```

## グループ化

### 拡張正規表現

拡張正規表現におけるグループを使うには、`-E` オプションを利用します。

`()` を利用して一致した部分を、\1, \2,.. などを用いて後方参照します。

```sh
$ echo 'hoge-pien-hoge' |\
 sed -E 's/(hoge)-[^-]*-\1/\1/g'
hoge

$ echo 'my number is 090-893-893' |\
 sed -E 's/(my number)[^0-9]*([-0-9]*)/\1: \2/'
my number: 090-893-893
```

### sed オリジナル

sed のオリジナルの表現として、一致した部分を & を使って参照することができます。

```sh
$ echo -e "#Title\n##SubTitle" | sed 's/^#*/& /g'
# Title
## SubTitle
```

### （おまけ）+ は基本正規表現では使えない

正規表現の `+` （直前の文字が１回以上）を使ってマッチさせようと思ったら、思ったような挙動をしなかったのでメモしておきます

```sh
# 期待する挙動 → # Title
$ echo -e "#Title\n##SubTitle" | sed 's/#+/& /g'
#Title
##SubTitle

# -E をつけて拡張正規表現にしてやるとうまくいく
$ echo -e "#Title\n##SubTitle" | sed -E 's/#+/& /g'
# Title
## SubTitle
```


## おわりに
今回は、最近知った sed の便利そうな機能を紹介しました。

他にも便利な使い方やオプションなどありましたら、ぜひ教えてください！