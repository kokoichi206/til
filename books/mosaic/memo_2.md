## sec 2
超解像ベースのモザイク除去

### 超解像技術
超解像技術とは、「以下に画像を綺麗に拡大するか」

- 低解像度の画像（LR）と高解像度の画像（HR）を用意
- LRはBicubic法など既存の画像処理で、HR画像を縮小して作成することが多い
- LR画像を元のHRの解像度まで拡大する。拡大結果を比較する。

### Nearest Neighbor 法とモザイク
最も簡単なモザイクのかけ方

- 元画像の1/Nの解像度にNearest Neighbor法で縮小する
- 縮小した画像を、Nearest Neighbor法で元の解像度まで拡大する。

Bicubic法もNearest Neighbor法も

画像の縮小や拡大において、一般に「Nearest Neighbor法 → Bilinear法 → Bicubic法」の順で綺麗になる。綺麗さと計算量はトレードオフ。
Nearest Neighborは最も軽いが汚い手法

#### モザイクと超解像技術
モザイク除去＝超解像問題と考えるのが最もシンプルなアプローチ

#### CNN と超解像技術
超解像技術とCNNの親和性は非常に高い。落とした情報を数学的に回復させることはできないが、学習ベースで条件付けて、元のHRに戻せるようにする。

> 超解像もモザイク除去もCNNが便利。

#### RSNR
超解像やモザイク除去を含め画像を出力とする場合は、いくつか専用の評価関数を使うことが多い。ここでの評価関数とは、分類問題の制度にあたるような関数である。**PSNR(ピーク信号対雑音比)**という指標が最も使われる

PSNRは画質の劣化を計測し、画像間の「歪み（Distortion）」を評価する指標の代表格。20dB以下だと雑音が目立つようになる

> PSNRとはピクセル間の平均二乗誤差ベースで測った、画質の定量指標

#### Subpixel-Conv(Pixel Shuffle)
チャンネル方向の厚みを空間方向に展開する！

#### 超解像問題としてのモザイク除去の限界
拡小後にガウシアンぼかし

#### 実装
- 入力にモザイク画像（32x32x3）
- カーネルサイズ4のMaxPoolingで、8x8の低解像度を作る（情報は落ちない）
- Conv2D 256ch カーネルサイズ=3 -> BN -> ReLU (8x8x256)
- 2倍のPixel Shuffle (16x16x64)
- Conv2D 256ch カーネルサイズ=3 -> BN -> ReLU (16x16x256)
- 2倍のPixel Shuffle (32x32x64)
- Conv2D 3ch カーネルサイズ=1 -> Sigmoid

##### データセット
uint8→float32へのキャストと、[0, 255]->[0, 1]へのスケール変換
これを行ってくれるのが、tf.image.convert_image_dtype

- from_tensor_slices((X, y))というデータセットに対して、X, yに処理を適用したいときは、dataset.map(...)という関数を使う。
- Keras APIで訓練する場合、訓練データは無限ループにする必要がある。.batchより前にrepeat()を入れる。
- テストデータは、repeat()もshuffle()も不要
- prefetch(buffer_size=tf.data.experimental.AUTOTUNE)は、事前にバッチデータを作成しておいて訓練を高速化するための設定

##### 評価
画像を出力とするケースでは評価関数にPSNRを用いると、回復の状況を定量的に測定できてわかりやすい

PSNRは画像のピクセル値が[0, 1]スケールの時、次の式

$$
PSNR=10\cdot \log_{10}\frac{1}{MSE}
$$

ここで$MSE$は２つのグレースケール画像間のL2距離（Mean Squared Error）


Validationのlossの最小値が更新されたときに係数を保存するには、

``` python
ckpt = tf.keras.callbacks.ModelCheckpoint("checkpoint/weights", save_best_only=True, save_weights_only=True)
```






