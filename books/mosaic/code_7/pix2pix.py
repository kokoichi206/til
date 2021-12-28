from sklearn.datasets import load_iris
import numpy as np

## SVD
data, target = load_iris(return_X_y=True)
U, S, V = np.linalg.svd(data)
print(S)
###

## Power Iteration による最大特異値
### Spectral Normalizationの論文ではPower Iterationの
### 反復回数は1回で十分であることが書かれている。
import matplotlib.pyplot as plt

def l2_normalize(x, eps=1e-12):
    return x / (np.sum(x ** 2) ** 0.5 + eps)

results = []
for p in range(1, 6):
    U = np.random.randn(1, data.shape[1])
    for i in range(p):
        V = l2_normalize(np.dot(U, data.T))
        U = l2_normalize(np.dot(V, data))
    sigma = np.dot(V, np.dot(data, U.T))
    results.append(sigma.flatten())
###

plt.plot(np.arange(1, 6), results)


!git clone https://github.com/koshian2/InpaintingUtils
!mv InpaintingUtils/*.py .
!rm -r InpaintingUtils


import tensorflow as tf
from inpainting_layers import ConvSN2D

inputs = tf.random.normal((16, 256, 256, 3))
x = ConvSN2D(64, 3, padding="same")(inputs)
###

print(x.shape)


## model の構成
from inpainting_layers import InstanceNorm2D
import tensorflow.keras.layers as layers

## block_D
inputs_g = layers.Input((256, 256, 3))
x = ConvSN2D(64, 3, strides=2, padding="same")(inputs_g)
x = InstanceNorm2D()(x)
x = layers.ReLU()(x)

block_G = tf.keras.models.Model(inputs_g, x)

## block_D
inputs_d = layers.Input((256, 256, 3))
x = ConvSN2D(64, 3, strides=2, padding="same")(inputs_d)
x = layers.ReLU()(x)

block_D = tf.keras.models.Model(inputs_d, x)
###

block_G.summary()
block_D.summary()


## Google Driveとデータのロード
from google.colab import drive
drive.mount("gdrive")
## データの読み込み
!cp gdrive/My\ Drive/colab\ data/kaggle.json kaggle.json
!mkdir /root/.kaggle/
!cp kaggle.json /root/.kaggle/kaggle.json
!kaggle datasets download -d splcher/animefacedataset
!unzip animefacedataset.zip > /dev/null

## TPU下準備
import tensorflow as tf
import os
tpu_grpc_url = "grpc://" + os.environ["COLAB_TPU_ADDR"]
tpu_cluster_resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu_grpc_url)
tf.config.experimental_connect_to_cluster(tpu_cluster_resolver) # TF2.0の場合
tf.tpu.experimental.initialize_tpu_system(tpu_cluster_resolver) # TF2.0の場合、今後experimentialが取れる可能性がある    
strategy = tf.distribute.experimental.TPUStrategy(tpu_cluster_resolver) 


# 作ってもらっている中身から import する。========！自分で作ってみる！========
from biggan_model import image_to_image_generator, discriminator

### Noneを埋めよ
with strategy.scope():
    model_G = image_to_image_generator()
    model_D = discriminator()

    model_G.summary()
    model_D.summary()
###


# Hinge loss の def
## Adversarial Loss（ 𝐿𝑎𝑑𝑣 ）
import numpy as np
def hinge_loss(logits, loss_type):
    assert loss_type in ["gen", "dis_real", "dis_fake"]
    if loss_type == "gen":
        return -tf.reduce_mean(logits, axis=(1, 2, 3))
    elif loss_type == "dis_real":
        # minval = tf.minimum(logits - 1, tf.zeros(logits.shape, dtype=logits.dtype)) # 本文での参考回答例
        minval = tf.minimum(logits -1,tf.zeros(tf.shape(logits),dtype=logits.dtype)) # 修正
        return -tf.reduce_mean(minval,axis=(1,2,3))
    else:
        # minval = tf.minimum(-logits - 1, tf.zeros(logits.shape, dtype=logits.dtype)) # 本文での参考回答例
        minval = tf.minimum(-logits-1,tf.zeros(tf.shape(logits),dtype=logits.dtype)) # 修正
        return -tf.reduce_mean(minval,axis=(1,2,3))
## 確認用
testval = np.arange(-2.0, 2.1, 0.25).reshape(-1, 1, 1, 1)
print("gen:", hinge_loss(testval, "gen"))
print("dis_real:", hinge_loss(testval, "dis_real"))
print("dis_fake:", hinge_loss(testval, "dis_fake"))


# Generator, Discriminator の損失関数
## 出力が1階テンソルとなるようなL1ロスを定義せよ
def l1_loss(y_true, y_pred):
    return tf.reduce_mean(tf.abs(y_true - y_pred), axis=(1, 2, 3))

class Losses:
    @staticmethod
    def generator_loss(embed_fake, img_real, img_fake):
        # adversarial loss
        loss_adv = hinge_loss(embed_fake, "gen")
        # L1 loss
        loss_l1 = l1_loss(img_real, img_fake)
        return loss_adv + 100 * loss_l1

    @staticmethod
    def discriminator_loss(embed_real, embed_fake):
        return hinge_loss(embed_real, "dis_real") + hinge_loss(embed_fake, "dis_fake")
    ### 

## 確認用
testval = np.arange(-2.0, 2.1, 0.25).reshape(-1, 1, 1, 1)
dummy_img = np.ones((testval.shape[0], 32, 32, 3), dtype=testval.dtype)
print("G_loss :", Losses.generator_loss(testval, dummy_img, dummy_img + 0.5))
print("D_loss :", Losses.discriminator_loss(testval, testval[::-1]))


# データセットの用意
import glob
from PIL import Image
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def load_dataset(batch_size):
    # animeface
    anime_faces = sorted(glob.glob("images/*.jpg"))
    anime_orig = []
    anime_mosaic = []
    for path in anime_faces:
        with Image.open(path) as img:
            orig = img.resize((64, 64), Image.LANCZOS)
            mosaic = orig.resize((2, 2), Image.NEAREST) # 強烈なモザイク
            mosaic = mosaic.resize((64, 64), Image.NEAREST)
            anime_orig.append(np.asarray(orig, np.uint8))
            anime_mosaic.append(np.asarray(mosaic, np.uint8))
    anime_orig = np.asarray(anime_orig)
    anime_mosaic = np.asarray(anime_mosaic)

    train_orig, test_orig, train_mosaic, test_mosaic = train_test_split(anime_orig, anime_mosaic, test_size=0.15, random_state=18)    

    def preprocess(inputs):
        x = tf.image.convert_image_dtype(inputs, tf.float32)
        return x * 2.0-1.0        
    # dataset
    train_set = tf.data.Dataset.from_tensor_slices((train_orig, train_mosaic)).map(lambda *args: [preprocess(a) for a in args])
    train_set = train_set.shuffle(1024).batch(batch_size,drop_remainder=True).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    test_set = tf.data.Dataset.from_tensor_slices((test_orig, test_mosaic)).map(lambda *args: [preprocess(a) for a in args])
    test_set = test_set.shuffle(1024).batch(batch_size,drop_remainder=True).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    return train_set, test_set

## 可視化用
train_set, _ = load_dataset(256)
orig, mosaic = next(iter(train_set))
fig = plt.figure(figsize=(14, 14))
for i in range(50):
    ax = fig.add_subplot(10, 10, i*2+1)
    ax.imshow(mosaic[i]*0.5+0.5)
    ax.axis("off")
    ax = fig.add_subplot(10, 10, i*2+2)
    ax.imshow(orig[i]*0.5+0.5)
    ax.axis("off")


# TPUのstrategyのスコープで、ネットワーク、オプティマイザー、データセットの準備をする。
# オプティマイザーはDもGも学習率0.0002（2e-4）のAdam
batch_size = 256
train_set, test_set = load_dataset(batch_size)

with strategy.scope():
    model_G = image_to_image_generator()
    model_D = discriminator()

    optim_G = tf.keras.optimizers.Adam(lr=2e-4)
    optim_D = tf.keras.optimizers.Adam(lr=2e-4)
    
    train_set = strategy.experimental_distribute_dataset(train_set) 
    test_set = strategy.experimental_distribute_dataset(test_set) 


# 訓練ループ. train
from utils import make_grid, distributed, Reduction
import utils
utils.strategy = strategy

with strategy.scope():
    @distributed(Reduction.SUM, Reduction.SUM)
    def train_on_batch(img_real, img_mosaic):
        with tf.GradientTape() as d_tape, tf.GradientTape() as g_tape:
            img_fake = model_G(img_mosaic, training=True)

        # train D
        with d_tape:
            y_real = model_D(img_real, training=True)
            y_fake = model_D(img_fake, training=True)
            d_loss = Losses.discriminator_loss(y_real, y_fake)
            d_loss = tf.reduce_sum(d_loss, keepdims=True) * (1.0 / batch_size)
        grads = d_tape.gradient(d_loss, model_D.trainable_weights)
        optim_D.apply_gradients(zip(grads, model_D.trainable_weights))
        
        # train G(A)
        with g_tape:
            y_fake = model_D(img_fake, training=False)
            g_loss = Losses.generator_loss(y_fake, img_real, img_fake)
            g_loss = tf.reduce_sum(g_loss, keepdims=True) * (1.0 / batch_size)
        grads = g_tape.gradient(g_loss, model_G.trainable_weights)
        optim_G.apply_gradients(zip(grads, model_G.trainable_weights))                
        return g_loss, d_loss
###

# 訓練ループ. validation
with strategy.scope():
    @distributed(Reduction.MEAN, Reduction.CONCAT, Reduction.CONCAT)
    def validation_on_batch(img_real, img_mosaic):
        img_fake = model_G(img_mosaic, training=False)
        psnr = tf.image.psnr(img_real, img_fake, max_val=2.0)
        psnr = tf.reduce_mean(psnr, keepdims=True)
        return psnr, img_mosaic, img_fake
###
