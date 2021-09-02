```sh
$ sudo apt install cpanminus

$ cpanm App::csv2tsv
$ cpanm App::csel
$ cpanm App::expandtab
$ cpanm App::crosstable
$ cpanm App::colsummary
$ cpanm App::venn
$ cpanm App::digitdemog
$ cpanm App::colgrep
```

```perl
$ perl -E 'say join"\t",1..12'
```

## Perl 入門
```perl
# -e でワンライナーで利用
$ perl -e 'print "Hello,World\n";'
# -l で \n を省略
$ perl -le '$string = "Hello,World";for(1..3){print $string;}'
$ perl -le '$string = "Hello,World";for(1..3){print $string;}'
```

```perl
$ cat hello_test.txt
Hello,World1
Hello,World2
Hello,World3
Hello,World4
Hello,World5
Hello,World6
Hello,World7
Hello,World8
Hello,World9
Hello,World10
# -n: １行ずつ処理する
$ cat hello_test.txt | perl -nle '$i++;if($i%3==0){print "$i:$_";}'
3:Hello,World3
6:Hello,World6
9:Hello,World9
```

### オプション
- -e
  - ワンライナーで使用
- -l
  - \n を省略
- -n
  - 行ごとに処理だけする
  - マッチする行だけ出力する
- -p
  - 行ごとに処理し、出力
  - 置換？ sed みたいな？
- -a
  - awk っぽくする？
  - いい感じに行をカラムに分割する
- -F
  - -a オプションで分割時の区切り文字を指定する
- -i
  - ファイルを編集し、バックアップを作成する
