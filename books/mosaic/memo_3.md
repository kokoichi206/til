## sec 3
U-Net によるモザイク除去

Image to image translation のタスクで頻繁に使われる「U-Net」というCNNのモデルがある

### Image to image translation: I2I
入力画像を条件として画像を出力する

I2Iの例

- ノイズ軽減（Noise reduction）
- 超解像（Super resolution）
- 条件なしの画像生成（Unconditional synthesis）
  - DCGAN, BigGAN
  - ノイズから画像を生成するようなモデル
- モダリティーの変換（Cross modality synthesis）
  - pix2pix, Cycle GAN
  - 白黒画像をカラー画像に変換する
  - 線画を着色する

### U-Net
Uの字になっているからU-Netと言われる。
Encoder to Decoder。U-Netの大きな特徴として、EncoderとDecoderの間の**Skip-Connection**がある。
ここの**Skip-Connection**は、ResNetの2~4層の畳み込みレイヤーごとのものよりも、**もっと長いスパン**

ここでのSkip-Connectionは、**画像を使い回しできるところは使おうという、コピペの意味合い**が強い。

``` python
import tensorflow.keras.layers as layers
## ResNet
x = layers.Add()([x, respath])
## U-Net
x = layers.Concatenate()([x, enc_layer])
```

#### 実装
``` python
inputs = layers.Input((64, 64, 3))
e = layers.Conv2D(64, 5, paddinig="same",
            strides=4, activatoni="relu")(inputs) # 16*16*64
x = layers.Conv2D(128, 3, padding="same", activation="relu")(e)
x = layers.Concatenate()([x, e]) # 16*16*192
x = layers.Conv2D(64, 5, padding="same", activation="relu")(x)
x = layers.UpSampling2D(4)(x) # 64*64*64
x = layers.Concatenate()([x, inputs]) # 64*64*67
x = layers.Conv2D(3, 3, padding="same", activation="sigmoid")(x)

model = tf.keras.models.Model(inputs, x)
```

#### Pros and Cons

##### pros
- とにかくロスの収束が早い。Skip-Connectionを貼っただけでPSNRなどの評価指標が目に見えて改善する

##### cons
- GPUメモリを食いがち。OOMになりやすく、バッチサイズを大きくしづらい
  - Concatenateでメモリを無駄に食う
- 浅い層の特徴量をコピペするだけでそれっぽい画像ができるので、ネットワークが怠けてしまい、ボトムの訓練が進みづらいとも

### CNNの局所性
CNNは局所的な特徴を見がちで、CNNは画像全体の特徴を捉えることは必ずしも保証できない。

> CNNの位置普遍性という特徴。同時に畳み込みカーネルの性質から、局所的な特徴に注目しがち

### Squeeze and Excitation
CNNのモジュール。

被写体の形状や、全体の特徴を見るように補正しているらしい。。。

SE-Net

### Dilated Conv
Squeeze and Excitation の他にも広域の特徴を見ようとする試みがある。**Dilated Conv**（穴あきConv）もその１つ。

カーネルサイズを変えずに参照範囲だけ広げる

エッジのような高周波帯の特徴が失われないようにしつつも、広範囲を参照したい！という思想


### 演習
> globコマンドは処理系（Linux、Windows等）によってファイルの順番の保証されないので、パスでソートし順番を保証することを癖にしておこう。これを怠るとTrain Testの分割でリークのバグを引き起こすおそれがある。

#### 訓練データを作る
1. 本物の画像をリサイズ（64x64）し、Numpy配列で格納する
2. 1.で作成したNumpy配列に対して、モザイクを付与する
3. 1.2.で作成したNumpy配列に対して、Train Testの分割をする

##### 1.
``` python
import numpy as np

ground_truths = []
for path in image_paths:
    with Image.open(path) as img:
        if img.width < 64 or img.height < 64:
            continue
        img = img.resize((64, 64), Image.LANCZOS)
        ground_truths.append(np.array(img, np.uint8))
###
ground_truths = np.asarray(ground_truths)
print(ground_truths.shape, ground_truths.dtype)
```

##### 2.
``` python
from PIL import ImageFilter

mosaics = []
for i in range(ground_truths.shape[0]):
    with Image.fromarray(ground_truths[i]) as img:
        mosaic = img.resize((img.width//4, img.height//4), Image.NEAREST)
        mosaic = mosaic.filter(ImageFilter.GaussianBlur(1.5))
        mosaic = mosaic.resize(img.size, Image.NEAREST)
        mosaics.append(np.asarray(mosaic, np.uint8))

mosaics = np.asarray(mosaics)
print(mosaics.shape, mosaics.dtype)

fig = plt.figure(figsize=(14, 14))
for i in range(100):
    ax = fig.add_subplot(10, 10, i+1)
    ax.imshow(mosaics[i])
    ax.axis("off")
```

##### 3.
``` python
from sklearn.model_selection import train_test_split

gt_train, gt_test, mosaic_train, mosaic_test = train_test_split(ground_truths, mosaics, test_size=0.15, random_state=18)
###
print(gt_train.shape, gt_test.shape)
print(mosaic_train.shape, mosaic_test.shape)
```

#### Pixel Shuffle
``` python
### 以下の空欄を埋めよ（passは削除せよ）
def pixel_shuffle(inputs, out_ch):
    x = layers.Conv2D(out_ch*4, 1, activation="relu")(inputs)
    x = layers.Lambda(lambda z: tf.nn.depth_to_space(z, 2))(x)
    return x
###

## テスト用
inputs = layers.Input((64, 64, 128))
x = pixel_shuffle(inputs, 64)
model = tf.keras.models.Model(inputs, x)
model.summary()
```

#### COnv2D -> Batch Normalization -> ReLU
``` python
### 以下の空欄を埋めよ（passは削除せよ）
def conv_bn_relu(inputs, ch, dilation_rate):
    x = layers.Conv2D(ch, 3, padding="same", dilation_rate=dilation_rate)(inputs)
    x = layers.BatchNormalization()(x)
    return layers.ReLU()(x)
###

## 確認用
inputs = layers.Input((64, 64, 128))
x = conv_bn_relu(inputs, 64, 1)
model = tf.keras.models.Model(inputs, x)
model.summary()
```

#### U-Net
NchのConv2Dレイヤーを「Conv N」と表記する。例えば、Conv 64とは、64chの畳み込みレイヤーである。各Convレイヤーには特記がない限りBatch NormalizationとReLUを入れる（Conv-BN-ReLUという順番で良い）

#### TPUのおまじない
``` python
import tensorflow as tf
import os
tpu_grpc_url = "grpc://" + os.environ["COLAB_TPU_ADDR"]
tpu_cluster_resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu_grpc_url)
tf.config.experimental_connect_to_cluster(tpu_cluster_resolver) # TF2.0の場合
tf.tpu.experimental.initialize_tpu_system(tpu_cluster_resolver) # TF2.0の場合、今後experimentialが取れる可能性がある    
strategy = tf.distribute.experimental.TPUStrategy(tpu_cluster_resolver) 
```

#### 損失関数の　def
``` python
def loss_function(y_true, y_pred):
    return tf.reduce_mean(tf.abs(y_true-y_pred), axis=(1,2,3))
###

## 確認用
tf.random.set_seed(18)
x1 = tf.random.uniform((8, 64, 64, 3))
x2 = tf.random.uniform((8, 64, 64, 3))
print(loss_function(x1, x2))
```

#### 評価関数の　def
``` python
def psnr(y_true, y_pred):
    return tf.image.psnr(y_true, y_pred, max_val=1.0)
###

## 確認用
tf.random.set_seed(18)
x1 = tf.random.uniform((8, 64, 64, 3))
x2 = tf.random.uniform((8, 64, 64, 3))
print(psnr(x1, x2))
```

#### dataset
``` python
def preprocess(inputs):
    return tf.image.convert_image_dtype(inputs, tf.float32)
### 

## 確認用
x = preprocess(np.arange(64*64*3).reshape(64,64,3).astype(np.uint8)).numpy()
print(x.shape, x.dtype, np.min(x), np.max(x))
```

#### 訓練データの準備
``` python
# trainset = tf.data.Dataset.from_tensor_slices((mosaic_train, gt_train)).map(
#     lambda *args: [preprocess(a) for a in args]
# ).shuffle(1024).batch(256).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
# testset = tf.data.Dataset.from_tensor_slices((mosaic_test, gt_test)).map(
#     lambda *args: [preprocess(a) for a in args]
# ).batch(256).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)    
###

trainset = tf.data.Dataset.from_tensor_slices((mosaic_train, gt_train)).map(
    lambda *args: [preprocess(a) for a in args]
).shuffle(1024).batch(256, drop_remainder=True).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
testset = tf.data.Dataset.from_tensor_slices((mosaic_test, gt_test)).map(
    lambda *args: [preprocess(a) for a in args]
).batch(256, drop_remainder=True).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
```





