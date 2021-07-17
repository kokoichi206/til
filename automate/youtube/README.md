# youtubeで遊ぼう
[参考URL](https://qiita.com/ryoya41/items/dd1fd4c1427ece787eea)

## Requirements
google-api-python-client==1.9.3

```
pip3 install google-api-python-client==1.9.3
```

## 流れ
1. GCP（Google Cloud Platform）にて、YouTube Data API v3のAPI Key取得
2. 次にPython言語を利用して、はじめに特定チャンネルのChannel IDを取得
3. Channel IDを利用して特定チャンネルの各種データ（チャンネルタイトル、登録者数、動画本数、開始日時）を取得し、チャンネル用csvファイルを出力
4. さらに同様のChannel IDを利用して、特定チャンネルから投稿されている各動画からVideo IDを取得し、その各動画のVideo IDに紐づく各種データ（動画タイトル、再生数、高評価、低評価、コメント数、投稿日時）を抜き出し、ビデオ用csvファイルを出力

