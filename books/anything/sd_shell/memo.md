下のようなひねくれたコマンドにも対応しないといけない！  
（読めない、、、）

```sh
echo あいう"$( function a() { echo エオ | rev ; }; ( (a) | a) | a)"

a () for a in date{,}; do sleep 3 | $a | rev ; done ; a


# cf
echo あいう"$( function a() { echo エオ | rev ; }; (a) )"
a () for a in date{,}; do sleep 3 | $a | rev ; done
```

setup

```sh
brew install rust

cargo --version
cargo 1.64.0 (387270bc7 2022-09-16)
```

run

```sh
cargo run
```

```rust
// :? はデバッグようにデータを文字列で出力するための指定
print!("{:?}", words);
```

トレース

```sh
# ~/file_log にシステムコールの記録を保存する。
strace ./binary_file 2> ~/file_log
```

execve では、それまでのプログラムを破棄し、同じプロセス内で別のプログラムを立ち上げる。  
（そのプログラムの実行が終わっても元のところには帰れない。）

Bash はあるしかけで、自身が消えるのを避けている。
