## Android
Android 側で気をつけること

### TextView に値をセットするとき
TextView.setText(XXX)

で、XXX に Int を入れてもコンパイルエラーは出ないが、以下のようにラッピングしてあげる必要がある！

```java
dateView.setText(String.valueOf(mi_age));
 ```

### Web 通信
- HttpURLConnection

#### post で画像を送るときは？？？
- https://stackoverflow.com/questions/11766878/sending-files-using-post-with-httpurlconnection
  - うまくいかず
  - Broken pipe ERROR
- OutputStream に書き込む？
  - HTML から送った時と同じ形式で、name: img -> value: *file* で送ってみる？
  - FileStream とか使う？？
- multipart/form-data?
  - [-- に注意](https://qiita.com/Zaki_Tk/items/073f597d52f6fd8e3dcd)
  - [rfc2388](https://www.ietf.org/rfc/rfc2388.txt)
- bitmap to png @ python
- 普通の HTML の from から送ったときのファイル形式
  - 受け取りは request.files で行っている

```bash
ImmutableMultiDict([('img', <FileStorage: 'スクリーンショット 2021-09-19 14.00.03.png' ('image/png')>)])
```

- outPutStream に、画像を載せる
  - API を叩く側（今回の Android）から見たら、画像の方が output（出ていくデータ）
- inPutStream に応答が返ってくる！


