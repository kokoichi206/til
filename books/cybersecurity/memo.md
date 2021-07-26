# メモ

## sec1
実行可能なコマンド３つ

- ファイル
- 組み込みコマンド（built-in）
  - 高速
- 予約後（keyword）

```sh
$ type -t if
keyword
$ type -t pwd
builtin

# -k: 予約語 -c: コマンド -b: builtin
$ compgen -k
```

標準入出力のリダイレクト

```sh
$ handywork < data.in > results.out 2> err.msgs
$ handywork < data.in > results.out 2>&1
# これは上と一緒
$ handywork < data.in &> results.out

# 追記にしたい時
$ handywork < data.in &>> results.out
```

コマンドのバックグラウンド実行
```sh
$ ping 8.8.8.8 &> ping.log &
$ jobs
$ fg TASK_NUM
```

