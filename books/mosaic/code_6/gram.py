from sklearn.datasets import load_iris
import numpy as np

data, target = load_iris(return_X_y=True)
print(data.shape)
## 相関行列
print(np.corrcoef(data, rowvar=False))
###

## 分散共分散行列
print(np.cov(data, rowvar=False, ddof=0))
###

## グラム行列
print(np.dot(data.T, data))
###

## グラム行列から分散共分散行列
mu = np.mean(data, axis=0, keepdims=True)
cov_data = data - mu
print(np.dot(cov_data.T, cov_data)/data.shape[0])
###

## グラム行列から相関関数
sigma = np.std(data, axis=0, keepdims=True)
corr_data = (data - mu) / sigma
print(np.dot(corr_data.T, corr_data) / data.shape[0])
###



# ================= P-Conv ==================
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



!curl -LO http://download.tensorflow.org/example_images/flower_photos.tgz
!tar xzf flower_photos.tgz > /dev/null


# 128x128にリサイズ
# ランダムな太さの直線を引いている。 ⇦ これはどういう処理？
from PIL import Image, ImageDraw
import glob
import matplotlib.pyplot as plt

img_true, img_mask, mask = [], [], []
paths = sorted(glob.glob("flower_photos/*/*.jpg"))
for p in paths:
    with Image.open(p) as img, Image.new("L", (128, 128), color=255) as m:
        img = img.resize((128, 128), Image.LANCZOS)
        img_true.append(np.asarray(img, np.float32))
        draw_img = ImageDraw.Draw(img)
        draw_mask = ImageDraw.Draw(m)
        for s, d, w in zip(np.random.uniform(0, 128, 10), np.random.uniform(0, 128, 10), np.random.uniform(0, 10, 10)):
            draw_img.line((0, int(s), 128, int(d)), fill=(255, 255, 255), width=int(w))
            draw_mask.line((0, int(s), 128, int(d)), fill=0, width=int(w))
        img_mask.append(np.asarray(img, np.float32))
        mask.append(np.asarray(m, np.float32))

img_true = np.asarray(img_true) / 255.0
img_mask = np.asarray(img_mask) / 255.0
mask = np.expand_dims(np.asarray(mask) / 255.0, axis=-1)

print(img_true.shape, img_mask.shape, mask.shape)

# データの確認
fig = plt.figure(figsize=(14, 14))
for i in range(27):
    for j, x in enumerate([img_true, img_mask, mask]):
        ax = fig.add_subplot(9, 9, i*3+j+1)
        if x.shape[-1] == 3:
            ax.imshow(x[i])
        else:
            ax.imshow(x[i,:,:,0])
        ax.axis("off")

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


def psnr(y_true, y_pred):
    return tf.image.psnr(y_true, y_pred, max_val=1.0)

## モデルの訓練
model = create_model()
model.compile("adam", "mean_absolute_error", [psnr])
model.fit([img_mask, mask], img_true, batch_size=64, epochs=30)
###


## 結果確認
y_pred = model.predict([img_mask, mask])[:100]

fig = plt.figure(figsize=(14,14))
for i in range(50):
    ax = fig.add_subplot(10,10,2*i+1)
    ax.imshow(img_mask[i])
    ax.axis("off")
    ax = fig.add_subplot(10,10,2*i+2)
    ax.imshow(y_pred[i])
    ax.axis("off")





