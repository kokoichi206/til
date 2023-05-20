## cgroup

v1, v2 なるものがある

- 2006 に Google のエンジニアによって最初のパッチ
- Control Group
- cgroup v1: 2.6.24 のカーネルから
  - 当時、カーネルにコンテナ関連の機能載せるハードルが高かったため、汎用性を持たせた実装になっている
  - 問題点を改良した v2 が 4.5 カーネルで実装された

概要

- プロセスをグループ化して、そのグループ内に存在するプロセスに対して共通の管理を行う
- cgroup は機能の名前
  - プロセスをグループ化したグループの名前も cgroup と呼ぶ

## ファイルシステム

- cgroup ファイルシステム、という仮想的なファイルシステムをマウントし、その中にファイル・ディレクトリを使って操作する
- cgroup ファイルシステムは `/sys/fs/cgroup` 以下にマウントする

以下のコマンドは、Alpine Linux で行う！  
(デフォルトでは cgroup ファイルシステムをマウントしないため)

``` sh
# docker-compose
dc up
dc exec alpine /bin/sh

# もしくは、以下の docker
docker run -d --name my_alpine alpine:latest tail -f /dev/null
docker exec -it my_alpine /bin/sh

apk update apk
apk add sudo

# cgroup について
# 下をやろうとしたけど、なんか container 内の permission 関係で上手くいかなかった。
sudo mount -t tmpfs cgroup /sys/fs/cgroup
sudo mkdir /sys/fs/cgroup/cpu

sudo mount -t cgroup -o cpu cgroup /sys/fs/cgroup/cpu
mount: /sys/fs/cgroup/cpu: cgroup already mounted on /sys/fs/cgroup/systemd.
```



## net_prio　コントローラー

- Linux では、通信を行うためにソケットが作られる
  - そこに対してファイルの入出力が行われる
- ネットワークトラフィックの優先度の指定
  - アプリケーションのコードで、優先度の指定としえt `SO_PRIORITY` とかを指定できる

## blkio コントローラー

- cgroup に属するタスクがブロ区デバイスに対して行う I/O の制御
- どのくらいぶろくデバイスへのアクセスを行ったかの統計量の取得
- ダイレクト I/O?
- ディスクアクセスはメモリアクセスに比べて非常に遅い
  - ページキャッシュという仕組みで、なるべく高速にアクセスできるようにしている
    - つまり、通常のファイル I/O はメモリーを介して行っている
- ダイレクト I/O
  - 通常のファイル I/O では、メモリを介して行うが、プロセス自身で制御したい時もあるよね
    - **ダイレクト I/O**
  - プロセスが直接 I/O を行うので、blkio コントローラーによる制御の出番
- ページキャッシュ
  - ライトバック処理
    - ページキャッシュからディスクへの書き込み
    - dirty 状態の解消




