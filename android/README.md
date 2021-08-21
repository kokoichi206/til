# Android MEMO

## adb commands

### 動画
```sh
$ adb shell screenrecord /sdcard/hoge.mp4
$ adb pull /sdcard/hoge.mp4
```

ただしこれだと音声が入らないため、Android 11 以上であれば、標準の「スクリーンレコード機能」を使ったほうが良さそう

```sh
$ adb pull /storage/emulated/0/Movies/screen-20210822-075841.mp4
```
