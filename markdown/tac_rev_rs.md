# ターミナル上で文字の順番を入れ替える

[目次]

[:contents]

## 行の中で最初と最後を入れ替える

rev (=reverse) を使います

```sh
$ echo hoge | rev
egoh

$ echo "123 456" | rev
654 321
```

### 回文判定

これを用いると、回文判定もできそうです

```sh
$ word=hogehoge; [ $word = $(echo ${word} | rev) ] &&\
 echo "'${word}' is a palindrome"

$ word=refer; [ $word = $(echo ${word} | rev) ] &&\
 echo "'${word}' is a palindrome"
'refer' is a palindrome
```

## 行を入れ替える

ファイルや標準入力をしたから読みたい時に使います。cat の逆です。

```sh
$ seq 3
1
2
3
$ seq 3 | tac
3
2
1

$ echo -e "hoge\npien" | tac
pien
hoge

## （おまけ）seq START STEP END
$ seq 3 -1 1
3
2
1
```

## rs コマンド

BSD 系であれば、`rs`コマンドが使えるかと思います。

> rs — reshape a data array

マニュアルを見る限りかなりたくさんの操作が行えそうです。-T で転置できるのは便利そうです。

```sh
$ sudo apt install rs

# 5 文字ごとに整形して（横幅整えて）出力
## (cf) $ seq 30 | xargs -n 5
$ seq 30 | rs 0 5
1   2   3   4   5
6   7   8   9   10
11  12  13  14  15
16  17  18  19  20
21  22  23  24  25
26  27  28  29  30
# -T で行列の転置を行う
$ seq 30 | rs 0 5 | rs -T
1   6   11  16  21  26
2   7   12  17  22  27
3   8   13  18  23  28
4   9   14  19  24  29
5   10  15  20  25  30
```

使えそうなオプションがあれば是非教えてください。


## おわりに

