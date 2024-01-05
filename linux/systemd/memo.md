## sec 1

- systemd: Linux の基本的な構成要素を提供するソフトウェアスイート
  - PID 1 である systemd プロセス
  - systemd-udevd
- 歴史
  - 2010 最初のリリース
  - 2
  - 014 RHEL に統合
- systemd は世界征服をしている。。。

``` sh
man systemd.index

ls /etc/systemd/system/
cd /etc/systemd/system/
```

## sec 2

- unit
  - systemd の各種リソースの抽象化
  - unit の状態、unit 間での依存関係
  - 11種類
    - service, device, swap, path, socket, timer, ...
    - target
      - 何もしないが依存関係の整理に使われる

``` sh
man systemd.unit
```

- unit には system, user の区別がある
  - system
    - PID 1 の systemd が管理する unit
  - user
    - ユーザーごとにそのユーザーの権限で起動される systemd が管理する unit
    - gvfs, emacsserver, などなど

``` sh
# systemd が unit について扱う情報が表示される！？
# show をあまり人間が見る機会はない。
systemctl show chronyd.service
```

- unit file と呼ばれる設定ファイルを読み込んでメモリ上に unit を作成したり
  - 既存の設定ファイルから自動で変換 → 実行時に生成される unit file もある
    - `/run/systemd` 以下にある

``` sh
$ ls /run/systemd               
ask-password        generator.late  io.system.ManagedOOM  network    quotacheck  shutdown   unit-root
ask-password-block  inaccessible    journal               notify     resolve     system     units
fsck.progress       incoming        machines              private    seats       timesync   userdb
generator           inhibit         netif                 propagate  sessions    transient  users
```

- unit file
  - INI ファイル形式

## links

- [freedesktop wiki](https://www.freedesktop.org/wiki/Software/systemd/)
- [systemd.io](https://systemd.io/)
