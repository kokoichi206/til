## pixiv.jsonをランタイムにコピー
!cp gdrive/My\ Drive/colab\ data/pixiv.json pixiv.json

# Bounding Box のデータをダウンロードする
!git clone https://github.com/koshian2/OpyDataset
!mv OpyDataset/bbox.zip bbox.zip
!cp bbox.zip gdrive/My\ Drive/colab\ data/bbox.zip
!unzip bbox.zip > /dev/null



