## FHS

File ystem Hierarcy Standard: UNIX 系 OS におけるディレクトリ名とその内容を定めているもの！

| ディレクトリ名 |                FHS3.0                |
| :------------: | :----------------------------------: |
|     /etc/      |       ホスト固有のシステム設定       |
|     /usr/      |     共有される読み出し専用データ     |
|    /usr/bin    |       大部分のユーザ用コマンド       |
|   /usr/sbin    | 必須ではない標準的なシステムバイナリ |
| /usr/share/man |           マニュアルページ           |
|     /var/      |        可変的なデータファイル        |
|    /var/run    |        ランタイムの可変データ        |

## なんでも

- `/etc/sudoers` を編集することで、`sudo` コマンドに細かく設定をすることができる
  - 普通に編集すると、ミスがあった時に sudo コマンドが使えなくなってしまうので、`visudo` コマンドを使う！
    - 設定ミスがあった時に警告を出してくれる
- 設定ファイルを変更する前に、`.bak` や`.org`でバックアップを取る
  - original
  - `cp` コマンドも使える！
    - `cp --backup=numbered foo foo.org`

## apache

```sh
ps -ef | grep apache2
```

## ネットワーク

デフォルトゲートウェイの IP アドレスを確認

```sh
$ ip route
default via 192.168.0.1 dev eth0 proto static
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
172.18.0.0/16 dev br-5c981fdc530a proto kernel scope link src 172.18.0.1
192.168.0.0/24 dev eth0 proto kernel scope link src 192.168.0.113

$ ip addr show
```

### IP アドレスの固定化

DHCP のように動的に IP アドレスを割り当てるシステムでは、ある一定の時間で IP アドレスが変更されたり、ホストを再起動するたびに IP アドレスが変更されたりする可能性がある。

設定ファイルを変更したときは、どこを修正したかのコメントを残すと良い！？

```sh
$ cat /etc/netplan/99_config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: false
      dhcp6: false
      addresses: [192.168.0.113/24]
      gateway4: 192.168.0.1
      nameservers:
        addresses: [127.0.0.53, 8.8.8.8, 8.8.4.4]

$ sudo netplan apply
```

## システムかんり

```sh
# どれだけ稼働しているか
$ uptime
 06:35:23 up 80 days, 15:59,  0 users,  load average: 0.68, 0.38, 0.27

# カーネルログ（見方わからんのう。。。）
dmesg

ps -aef

top
```

## ユーザー

- root
- システムユーザー
  - Web サーバーやメールサーバー、各種サービスを実行するユーザー
- 一般ユーザー

パーミッションの順番、ファイルオーナー、ファイルグループ、その他のユーザー・

```sh
$ ls -l /usr/bin/passwd
-rwxr-xr-x  1 root  wheel  172608 Oct 28 17:43 /usr/bin/passwd
```

### SUID

set uid  
ファイル実行フラグに s がついていると、そのコマンドを実行した際に、実行したユーザーではなく所有者のアクセス権限が適応される。  
→ そのことにより、他ファイルへのアクセスが可能になったりする。

```sh
chmod u+s 実行ファイル
```

### su

su コマンドのオプション、

- `-c`: 成り代わったユーザーで実行するコマンドを指定
- `-l`: ログインシェルを起動するため、環境変数が再設定される！

### sudo

root や他ユーザーに成り代わってコマンドを実行できる。

`sh -c` を用いてコマンドの引数、リダイレクト含めて指定！

```sh
sudo sh -c "echo \"hogeee pieeen\" > /tmp/messages"
```

別のユーザーのシェルを使いたい時。

```sh
# 対象ユーザーのシェルを起動する
sudo -s

# ログインシェルを起動する → .profile 等読み込みが走る
sudo -i
```

`doas` コマンドも、`sudo` の代替として注目されている！

`chattr` コマンドを使えば、`sudo` を使ってもそのままでは削除できないようにすることは可能。

## ファイル

### ジャーナリング

ファイルシステムの耐障害性の機能。

ext4 と XFS で使われている。  
更新内容の適応をアトミックにして、、ファイルシステムの整合性を取っている！

### パッケージマネージャ

- Red Hat
  - 低レベル: rpm (Red Hat Package Manager)
  - 高レベル: yum (Yellowdog Updater Modified)
  - 高レベル: dnf (DaNdiFied yum)
- Debian
  - 低レベル: dpkg
  - 高レベル: apt (Advanced Package Tool)

info は show のエイリアス。

yum から dnf への移行。

```sh
# 見つからないコマンドに対して、こいつが呼ばれている
$ command_not_found_handle 'sl'
Command 'sl' is available in '/usr/games/sl'
sl: command not found

# ubuntu の OS アップデート
sudo apt do-release-upgrade
```

## パケット

カプセル化

- Ethernet の住所 MAC アドレス, 物理的なアドレス
- 論理的なアドレス IP アドレス, IPv4, IPv6bbb
- TCP とポート番号, URI

UNIX では全てがファイル、ソケットですらファイル！

## ネットワークコマンド

```sh
# 名前解決
dig kokoichi0206.mydns.jp

# 自らの IP
# lo というインターフェース＝「ループバックインターフェース」
ifconfig | grep 192.1

# 届いてる？
ping kokoichi0206.mydns.jp

# 道筋
traceroute kokoichi0206.mydns.jp
traceroute -n kokoichi0206.mydns.jp

# ルータまでの経路
route

# ネットワーク内の機器
arp -a

# パケットの流れ。。。
sudo tcpdump -n -i eth0
```

ルーティング

```sh
# デフォゲも表示されている
ip route show
```

## コマンド

`grep -a` でバイナリも読み込む！（アクセスログの解析！）

1 行目にのみ著作権表記を記入  
`sed -i '1i著作権表記' file.c`

これは sed の『行番号 + コマンド』というよくあるセット！

Clinet for URL = cURL

`jq --raw-output (-r)`

```sh
echo "hoge" | tee ファイル名

# Permission Denied
sudo echo 'aaaa' > /tmp/root_file
echo 'aaaa' | sudo tee /tmp/root_file
```

`tee` は上書き、`tee -a` は追記！

```sh
# `at` コマンドのデーモンである `atd` が起動している状態を作る.
echo "実行したいコマンド" | at 日時
at -f ファイルのパス 日時
```

```sh
# 現行環境でシェルスクリプトを実行！
# https://www.shell-tips.com/bash/source-dot-command/#gsc.tab=0
. ./test.sh

# : コマンド = 唯一エラーにならずに終了し出力なし！
```

Bash の変数は、コマンドラインに置かれた後は変数展開をした後でコマンド文字列として解釈される、なるほど！！！

`ctrl + u` で行頭までカット、`ctrl + y` でペースト

ssh のローカルフォワード  
`ssh -L 5911:127.0.0.1:5901 username@server`

lsof

## こまんど

```sh
find . -print

find / -maxdepth 2 -type d -print

find . -name .git -type d -print

find . -name .git -type d -exec echo hoge {} \;

# + を区切り引数にすると、発見したファイル/ディレクトリを
# コマンドの引数として重ねて、後にまとめて実行してくれる！（）
find . -name .git -type d -exec echo hoge {} +
```
