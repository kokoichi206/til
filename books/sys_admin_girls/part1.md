### ssh 接続
- -Y: X の転送指定
  - X: Linuxで画面の描画と乳直の受け取りを担当する仕組み
- -C: 通信内容の圧縮

```sh
$ ssh -Y -C user@192.xxx.~~
$ nautilus

$ ssh user@192.xxx.~~ command

$ scp 元 先
```

### tmux
- 仮想端末の1つ
- SSH 接続後に、`tmux`と打って作業を始めておくと、通信が突然途切れても安全
  - 復活の呪文は`tmux attach`



### Memo
- Global Regular Expression Print
- `tail -F`
- `if [ $? != 0 ]; then exit; fi`
- `date +%Y-%m-%d`, `date +%y%m%d`
  - 入子のことを考えるなら、コマンド置換は`$()`がベター
- `$ echo -e "1\n2\n3\n4\n5\n7\n9" | pee "head -n 3" "tail -n 3"`
