!kaggle datasets download -d splcher/animefacedataset

!unzip animefacedataset.zip > /dev/null
###
!ls images -1U | wc -l # ファイル数のカウント


import matplotlib.pyplot as plt
from PIL import Image
import glob

fig = plt.figure(figsize=(14, 14))
image_paths = sorted(glob.glob("images/*.jpg"))
for i in range(100):
    ax = fig.add_subplot(10, 10, i+1)
    ax.imshow(Image.open(image_paths[i]))
    ax.axis("off")



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


from PIL import ImageFilter

mosaics = []
for i in range(ground_truths.shape[0]):
    with Image.fromarray(ground_truths[i]) as img:
        mosaic = img.resize((img.width//4, img.height//4), Image.NEAREST)
        mosaic = mosaic.filter(ImageFilter.GaussianBlur(1.5))
        mosaic = mosaic.resize(img.size, Image.NEAREST)
        mosaics.append(np.asarray(mosaic, np.uint8))
###
mosaics = np.asarray(mosaics)
print(mosaics.shape, mosaics.dtype)

fig = plt.figure(figsize=(14, 14))
for i in range(100):
    ax = fig.add_subplot(10, 10, i+1)
    ax.imshow(mosaics[i])
    ax.axis("off")


from sklearn.model_selection import train_test_split

gt_train, gt_test, mosaic_train, mosaic_test = train_test_split(ground_truths, mosaics, test_size=0.15, random_state=18)
###
print(gt_train.shape, gt_test.shape)
print(mosaic_train.shape, mosaic_test.shape)


## sc-SE の実装
import tensorflow as tf
import tensorflow.keras.layers as layers

## 以下の空欄を埋めよ（passは削除せよ）
def sc_squeeze_and_excitation(inputs, ch):
    # cSE
    x = layers.GlobalAveragePooling2D()(inputs)
    x = layers.Dense(ch // 8, activation="relu")(x)
    x = layers.Dense(ch, activation="sigmoid")(x)
    x = layers.Reshape((1, 1, ch))(x)
    x = layers.Multiply()([inputs, x])
    # sSE
    y = layers.Conv2D(1, 1, activation="sigmoid")(inputs)
    y = layers.Multiply()([inputs, y])
    # add
    x = layers.Add()([x, y])
    return x
### 

## テスト用
inputs = layers.Input((64, 64, 128))
x = sc_squeeze_and_excitation(inputs, 128)
model = tf.keras.models.Model(inputs, x)
model.summary()

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



## U-Net def
def create_model():
    inputs = layers.Input((64, 64, 3))
    # エンコーダー
    encoders = []
    x = inputs
    for i in range(3):
        x = conv_bn_relu(x, 64*2**i, 1)
        x = conv_bn_relu(x, 64*2**i, 1)
        x = sc_squeeze_and_excitation(x, 64*2**i)
        encoders.append(x)
        x = layers.AveragePooling2D(2)(x)
    # 中間層
    for d in [1, 2, 4]:
        x = conv_bn_relu(x, 512, d)
        x = conv_bn_relu(x, 512, d)
    for i in range(2, -1, -1):
        x = pixel_shuffle(x, 64*2**i)
        x = layers.Concatenate()([x, encoders[i]])
        x = conv_bn_relu(x, 64*2**i, 1)
        x = conv_bn_relu(x, 64*2**i, 1)
        x = sc_squeeze_and_excitation(x, 64*2**i)
    # 出力層
    x = layers.Conv2D(3, 3, padding="same", activation="sigmoid")(x)

    return tf.keras.models.Model(inputs, x)
###

## 確認用
create_model().summary()



## TPUのおまじない
import tensorflow as tf
import os
tpu_grpc_url = "grpc://" + os.environ["COLAB_TPU_ADDR"]
tpu_cluster_resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu_grpc_url)
tf.config.experimental_connect_to_cluster(tpu_cluster_resolver) # TF2.0の場合
tf.tpu.experimental.initialize_tpu_system(tpu_cluster_resolver) # TF2.0の場合、今後experimentialが取れる可能性がある    
strategy = tf.distribute.experimental.TPUStrategy(tpu_cluster_resolver) 


def loss_function(y_true, y_pred):
    return tf.reduce_mean(tf.abs(y_true-y_pred), axis=(1,2,3))
###

## 確認用
tf.random.set_seed(18)
x1 = tf.random.uniform((8, 64, 64, 3))
x2 = tf.random.uniform((8, 64, 64, 3))
print(loss_function(x1, x2))


def psnr(y_true, y_pred):
    return tf.image.psnr(y_true, y_pred, max_val=1.0)
###

## 確認用
tf.random.set_seed(18)
x1 = tf.random.uniform((8, 64, 64, 3))
x2 = tf.random.uniform((8, 64, 64, 3))
print(psnr(x1, x2))

def preprocess(inputs):
    return tf.image.convert_image_dtype(inputs, tf.float32)
### 

## 確認用
x = preprocess(np.arange(64*64*3).reshape(64,64,3).astype(np.uint8)).numpy()
print(x.shape, x.dtype, np.min(x), np.max(x))


trainset = tf.data.Dataset.from_tensor_slices((mosaic_train, gt_train)).map(
    lambda *args: [preprocess(a) for a in args]
).shuffle(1024).batch(256).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
testset = tf.data.Dataset.from_tensor_slices((mosaic_test, gt_test)).map(
    lambda *args: [preprocess(a) for a in args]
).batch(256).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)    
###



