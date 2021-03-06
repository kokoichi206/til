# awk で uniq を実行する
awk の連想配列の機能を使って、（シンプルな）`uniq`コマンドと同様の機能を実装できることが分かったので紹介したいと思います。

## uniq コマンドとは
awk の前にまず、`uniq`コマンドの復習からしましょう。その名の通り、重複のないユニークな値のみを取り出すコマンドです。

注意点として、`uniq`に渡す前に各行がソートされている必要があります。そのため、`sort | uniq`で１セットだと思ってもらっても間違いないと思います。

```sh
# sort しておかないと失敗する
echo -e '1\n2\n4\n2\n1' | uniq
1
2
4
2
1

# まず `sort` で並び替えて、
$ echo -e '1\n2\n4\n2\n1' | sort -n 
1
1
2
2
4
# その後に `uniq` に渡してあげる
$ echo -e '1\n2\n4\n2\n1' | sort -n | uniq
1
2
4
$ echo -e 'a\nb\na' | sort | uniq
a
b
```

## awk による uniq の実装
先に uniq を実装する方法から紹介しておきます。

下に示すように、連想配列に

- 登録がなければ追加・出力
- 登録があれば何もしない

という作戦で、初見のもののみ出力するようにしています。

```sh
# echo -e 'a\nb\na' | sort | uniq
$ echo -e 'a\nb\na' | awk '!a[$0]++ {print $0}'
```

以下では上の中身について少し補足しておきます。

### 連想配列？
awk における連想配列とは、key: value のペアのことで、他の言語では「ハッシュや辞書」などと呼ばれているものです。

ハッシュ値で管理しているため、「検索の速度が速く、呼び出すときの順番が保存されていない」という特徴があります。

#### 使い方
それでは使い方を簡単にみてみましょう。

まず、`array[key]=value` の形を取ります。

```sh
# ID、名前の行が入力できたときを考える
$ echo -e "1 tanaka\n2 nakamura"
1 tanaka
2 nakamura

# このとき以下のようにして、連想配列 a に代入できます
$ echo -e "1 tanaka\n2 nakamura" \
| awk '{a[$1]=$2}END{for(id in a)print "id: " id "\tname:" a[id]}'
id: 2   name:nakamura
id: 1   name:tanaka
```

ちなみに awk にはインデックスで管理するような普通のリストのようなものはなく、連想配列しか存在しません

```sh
$ awk 'BEGIN {for(i=0; i<=10; i++){a[i]=i}; for(x in a){print x}}'
2
3
4
5
6
7
8
9
10
0
1
```

この連想配列を用いて、先程の sort の例では、`!a[$0]++`を `<pattern>` にとり、`a[$0]`が 0 の時のみ出力されるようにしています。

（後置`a++`はそこの行が（？）終わってからインクリメントされることに注意（下の例））

```sh
$ echo -e 'a\nb\na' | awk '{print a[$0]++, a[$0]}'
0 1
0 1
1 2
```

## おわりに
awk は一般のプログラミング言語に比べて機能は限られるものの、ターミナル上で行いたい作業は工夫次第で大体できるという優秀な子です。

使いこなせるようになって快適なワンライナー生活を送りましょう。
