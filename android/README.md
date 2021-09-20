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

### PC 上で実機を操作する！
- Chrome:
  - `chrome://inspect/#devices`
  - chrome 関連のもの
- scrcpy
  - `brew install scrcpy`
  - 実機を PC 上にエミュレータっぽく表示させる
  - 

## ML
- [Mediapipe](https://google.github.io/mediapipe/)
  - [How to use mediapipe](https://margaretmz.medium.com/hello-mediapipe-on-android-813fc0553d79)
- Encountered ERRORs
  - [ndk platform does not exist](https://github.com/google/mediapipe/issues/1281)
  - [bazel の Android Studio 開けた後からの手順](https://google.github.io/mediapipe/getting_started/android.html)
  - `fatal error: 'features.h' file not found #include <features.h>^~~~~~~~~~~~`
