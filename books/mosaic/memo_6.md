## sec 6
Partial Convolutions によるモザイク除去

Image Inpading for Irregulr Holes Using Partial Convolutions（Partial Convolutions, P-Conv）

### Non-GANベース(P-Conv 等)の利点
- 訓練するネットワークが一個なので訓練するのが簡単
    - GANは二個以上のネットワークを同時に訓練するのに対し、P-Convを含めNon-GANベースでは、訓練するネットワークは一個
    - 訓練が速い傾向がある
    - 「勾配消失」「モード崩壊」といったGAN特有の不安定性を回避できる
- Validationが明確に定義できる
    - GANは損失関数が動的
    - GANベースでは訓練してすぐのValidation lossの値と、最後の方でのValidation lossの値を単純に比較することができない！

以上のような点から、「とりあえずP-Convでやってみる」のような初手としてはかなり有力である。

### P-Convとは
Inpainting は画像補完のタスク一般を意味し、Inpainting の手法の１つが P-Conv という位置付けである。

Inpainting 特に P-Conv は、モザイクのように四角形状のマスクよりも、不規則なマスクの方が得意。

P-Convでは**入力画像とカーネルとマスク**の３要素から計算する

### マスクに対する畳み込み
Conv2Dと似ているが、マスクは0,1 のバイナリー値であるので、特殊な計算を行う

マスクされていない部分が１つでもあれば出力を１とする。

P-Conv では画像とマスクで２回の畳み込みを行なっているため、**係数やメモリサイズが倍になってしまう**というデメリットがある。そのため、バッチサイズを増やすことが難しい。

### P-Conv がやっていること
マスクに対する畳み込みにより、マスク（モザイク）領域は徐々に小さくなる。これと CNN のダウンサンプリング構造と合わせると強力に機能する。

### VGG を使った損失関数
P-Conv をはじめ、画像生成モデルでは**訓練済みNNを損失関数として使う**ことを行う。VGG16/19 を使うことがほとんど。Style Loss, Perceptual Loss など

- 訓練済みVGGを使う：訓練の途中でVGGは**訓練しない**
- GAN：訓練中に、損失関数としているもう一方のネットワークを訓練する

### グラム行列
ある正方行列$X$が与えられた時に、$X^TX$を求めることである。

これを損失関数で使う直感的なメリットは後で説明する。

> グラム行列とは、ある行列を転転置させたものと、自身の行列積

### より広域の情報を参照した損失関数
グラム行列の１つの成分は、**元の行列の縦一列、横一列それぞれの情報を持っている**！

L1ロスのような$Y-X$は要素間の計算なので、ピクセル単位では１対１対応。L1ロスの各要素は「周囲の点の情報」を一切持っていない。

> 損失関数にグラム行列を使うと。L1ロスでは計算できなかったより広域の関係性を加味できる

### 分散共分散行列、相関行列はグラム行列の特別な場合
直感的には、グラム行列は相関のようなものを考えている、とみなせる

- データを事前に（系列間の）平均で引いて、グラム行列の期待値を取ると、分散共分散行列と一致
- データを事前に（系列間の）平均で引いて標準偏差で割って、グラム行列の期待値を取ると、相関行列と一致

Style-loss：VGGの特徴量＋グラム行列による損失関数

### P-Conv の損失関数
６項目からなる。

### P-Conv U-Net
U-NetのConv2Dレイヤーを全てP-Convに置き換えたもの。（＋デコーダーの活性化関数にLeaky ReLUを使用している）

### Region-wise Conv / Regin Normalization
> マスク領域、非マスク領域の分布不一致対策に、Region-wise Conv、Regin Normといった、領域別のConvレイヤー、Normalizationレイヤーを使うといった手法がある


### P-Conv レイヤーの定義
入力は画像とマスクの2つとする。（詳しくは本書参考）

1. 画像とマスクの要素間の積を取る 2, 積を取ったものを、Conv2Dと同じ畳み込み計算をする。単純にするため、畳み込みカーネルは3で統一する。
2. マスク側を全て1のカーネルで畳み込み計算する。これがパッチ内の非マスク領域のピクセル数となる
3. 2を3で割る。0 divideしないよう微小量を分母に足すこと。
4. マスク側を非マスク領域が膨張するように畳み込み計算する。これはカーネルサイズ3, same paddingのMax Poolingでよい。

今Kerasの独自レイヤーを定義するため、Kerasの関数ではなくTensorFlowの低レベル関数（1章の画像の畳み込み計算で見たもの）を用いる

> TF関数を使う場合、padding="SAME"が大文字なことに注意する

``` python
import tensorflow as tf
import tensorflow.keras.layers as layers

class PConv2D(layers.Layer):
    def __init__(self, ch, strides):
        super().__init__()
        self.ch = ch
        self.strides = strides

    def build(self, inputs_shape):
        img_shape, mask_shape = inputs_shape
        self.img_weights = tf.Variable(tf.random.normal((3, 3, img_shape[-1], self.ch)), trainable=True)
        self.mask_weights = tf.ones((3, 3, mask_shape[-1], 1))

    def call(self, inputs):
        img, mask = inputs
        # 画像側の畳み込み
        x = img * mask
        x = tf.nn.conv2d(x, self.img_weights, self.strides, padding="SAME")
        m = tf.nn.conv2d(mask, self.mask_weights, self.strides, padding="SAME")
        x = x / (m + 1e-8) 
        # マスク側の畳み込み
        m = tf.nn.max_pool2d(mask, 3, self.strides, padding="SAME")
        return x, m
### 

### 確認用
l = PConv2D(16, 1)
x = tf.random.normal((8,64,64,3))
m = tf.random.normal((8,64,64,1))
x, m = l([x, m])
print(x.shape, m.shape)
```


### 前処理


### モデルの作成
簡単な7つのP-Conv層を持つモデルを定義しよう。次のようなEncoder-Decoder形式のモデルを定義

- Encoder: 常にstrides=2、64->128->256のチャンネル数が増える
- 中間層：ch=256, stride=1の層を1つ
- Decoder: 2倍のアップサンプリング、128->64->3とチャンネル数を減少

畳み込み層は全て先程定義したP-Convを用いるものとする。

``` python
def create_model():
    inputs_img = layers.Input((128, 128, 3))
    inputs_mask = layers.Input((128, 128, 1))
    strides = [2,2,2,1,-2,-2,-2]
    chs = [64,128,256,256,128,128,3]
    x, m = inputs_img, inputs_mask
    for s, c in zip(strides, chs):
        if s < -1:
            x, m = layers.UpSampling2D(abs(s))(x), layers.UpSampling2D(abs(s))(m)
        x, m = PConv2D(c, max(s, 1))([x, m])
        if c != 3:
            x = layers.BatchNormalization()(x)
            x = layers.ReLU()(x)
        else:
            x = layers.Activation("sigmoid")(x)
    return tf.keras.models.Model([inputs_img, inputs_mask], x)
###

create_model().summary()
```


