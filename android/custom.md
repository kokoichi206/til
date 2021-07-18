## OpenGapps
- バリアントは最低限のPlayストアしかないpico

## 流れ
- [大まかな流れ](https://pc-freedom.net/google/android/update-nexus5-to-the-latest-android-11/)
  - うまくいかないところあり
- [画像多め](https://www.getdroidtips.com/lineageos-18-1-nexus-5/)
- [文章のみだがめっちゃ詳しい](https://www.lineageos18.com/2021/01/nexus-5-android-11-lineageos-18-custom.html)

```bash
# 下のコマンドの後、Reboot mode選択
$ adb reboot bootloader
# LOCK STATE を unlockedにする
# https://source.android.com/setup/build/running?hl=ja
$ fastboot oem unlock
$ fastboot flash recovery twrp-3.5.2_9-0-hammerhead.img
# 以下のコマンドなどで、必要なものを転送する！
$ adb push hh_repartition+to+2go.zip /sdcard/
```

hh..のインストールが終わったら、、[Advanced] > [Terminal]で表示されるターミナルに

```bash
$ modify 
```

とうって、パーティションを変更させる！

TWRP が起動したら LineageOS と OpenGApps を Nexus5 に転送

転送が完了したら、先程のように TWRP の「Install」をタップし、転送した LineageOS をタップ。

画面が切り替わり、インストール一歩手前の画面になります。

「Add more zips」をタップし、 OpenGApps のファイルをタップします。

これで、 LineageOS と OpenGApps をインストールする準備ができました。

あとは画面下の「Swipe to confirm flash」をスワイプしてインストールを実行します。


インストールが終わったら、ホーム画面に戻り、メニュー一覧にある「Reboot」をタップし、表示された一覧の中から「System」をタップして Nexus5 を起動させます。

インストール直後に表示される「Reboot System」のボタンでも再起動はされますが、なんかうまく起動しなくなったりすることが多い気がするので、コチラでやっています。

-> お？再起動ループ？？

### 再起動ループ（？）なりました
- やったこと
  - 電源ボタン＋上（下）による再起動
  - 電源ボタン＋上＋下による再起動
  - 温めるとセーフモードで起動するかも？ってことで、ドライヤーで温めて起動
  - バッテリーを1分くらい外した後に起動


## ハマったところ
- コマンドが見つかりません
  - 音量up＋電源ボタンで選べる
  - apply update from ADB」を選択
- now send the package you want
  - terminalで`adb sideload ～～.zip`を打つ
    - 今回はopen_gapps....zip
- `FAILED (remote: 'not supported in locked device')`
  - Lock Stateを解除してあげないと〜〜

- adb reboot bootloaderで`error: no devices/emulators found`
  - 開発者モードになってない
  - ＋USBデバッグを有効に
