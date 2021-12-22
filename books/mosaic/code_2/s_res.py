import tensorflow as tf
import numpy as np

(X_train, y_train), (X_test, y_test) = tf.keras.datasets.cifar100.load_data()
###
print(X_train.shape, y_train.shape, np.max(y_train))
print(X_test.shape, y_test.shape, np.max(y_test))

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(14,14))
for i in range(100):
    ax = fig.add_subplot(10, 10, i+1)
    ax.imshow(X_train[i])
    ax.axis("off")


## 人工的なモザイク付与
from PIL import Image
X_train_mosaic = np.zeros(X_train.shape, dtype=X_train.dtype)
X_test_mosaic = np.zeros(X_test.shape, dtype=X_test.dtype)

# 画像をNumpy配列で入力として受け取り、モザイクかかったNumpy配列を出力する関数
def add_mosaic(image):
    with Image.fromarray(image) as img:
        width, height = img.size
        x = img.resize((width//4, height//4), Image.NEAREST)
        x = x.resize((width, height), Image.NEAREST)
        return np.asarray(x, image.dtype)
###

for i in range(X_train.shape[0]):
    X_train_mosaic[i] = add_mosaic(X_train[i])
for i in range(X_test.shape[0]):
    X_test_mosaic[i] = add_mosaic(X_test[i])

fig = plt.figure(figsize=(14,14))
for i in range(100):
    ax = fig.add_subplot(10, 10, i+1)
    ax.imshow(X_train_mosaic[i])
    ax.axis("off")

## 超解像ベースのモザイク除去
### Subpixel-conv, Pixel Shuffle
### チャンネル方向の幅を、縦横方向に変換している
### Keras APIで使うときはLambdaレイヤーでラップするのが良い
import tensorflow.keras.layers as layers
inputs = layers.Input((32,32,3))
x = layers.MaxPooling2D(4)(inputs)
for i in range(2):
    x = layers.Conv2D(256, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)
    x = layers.Lambda(lambda z: tf.nn.depth_to_space(z, 2))(x)
x = layers.Conv2D(3, 1, activation="sigmoid")(x)

model = tf.keras.models.Model(inputs, x)
###
model.summary()


trainset = tf.data.Dataset.from_tensor_slices((X_train_mosaic, X_train))
trainset = trainset.map(lambda *args: tuple([tf.image.convert_image_dtype(a, tf.float32) for a in args]))
trainset = trainset.repeat().shuffle(2048).batch(128).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
### Noneを入力せよ
testset = tf.data.Dataset.from_tensor_slices((X_test_mosaic, X_test))
testset = testset.map(lambda *args: tuple([tf.image.convert_image_dtype(a, tf.float32) for a in args]))
testset = testset.batch(128).prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
###

## 確認用
for i, (a, b) in enumerate(trainset):
    if i == 0:
        print("train batch", a.shape, b.shape)
    elif i >= X_train.shape[0]//128:
        break
for i, (a, b) in enumerate(testset):
    if i == 0:
        print("test batch", a.shape, b.shape)

gray_scale_ratio = np.array([0.2126, 0.7152, 0.0722], np.float32).reshape(1,1,1,3) / 255.0 # グレースケール + [0,1]変換
diff = np.sum(X_test_mosaic*gray_scale_ratio, axis=-1) - np.sum(X_test*gray_scale_ratio, axis=-1) # グレースケールでのピクセル差
mse = np.mean(diff**2, axis=(1,2)) # MSEの導出
psnr = 10.0*np.log10(1.0/mse) # mseを使って計算せよ
###
print(np.mean(psnr))

### Tensorflow を使った psnr
psnr_tf = tf.image.psnr(X_test_mosaic/255.0, X_test/255.0, max_val=1.0)
print(tf.reduce_mean(psnr_tf).numpy())

## 訓練
def psnr(y_true, y_pred):
    return tf.reduce_mean(tf.image.psnr(y_true, y_pred, max_val=1.0))

model.compile("adam", "mean_squared_error", [psnr])
### Validationのlossの最小値が更新されたときに係数を保存
ckpt = tf.keras.callbacks.ModelCheckpoint("checkpoint/weights", save_best_only=True, save_weights_only=True)
model.fit(trainset, validation_data=testset, steps_per_epoch=50000//128, callbacks=[ckpt], epochs=50)

## 結果の確認
model.load_weights("checkpoint/weights")
y_pred = model.predict(X_test_mosaic/255.0)

fig = plt.figure(figsize=(14,14))
for i in range(50):
    ax = fig.add_subplot(10,10,2*i+1)
    ax.imshow(X_test_mosaic[i])
    ax.axis("off")
    ax = fig.add_subplot(10,10,2*i+2)
    ax.imshow(y_pred[i])
    ax.axis("off")

## ガウシアン付きモザイク
from PIL import ImageFilter

X_test_soft_mosaic = np.zeros(X_test.shape, X_test.dtype)
for i in range(X_test.shape[0]):
    with Image.fromarray(X_test[i]) as img:
        width, height = img.size
        x = img.resize((width//4, height//4), Image.NEAREST)
        x = x.filter(ImageFilter.GaussianBlur(1))
        x = x.resize((width, height), Image.NEAREST)
        X_test_soft_mosaic[i] = np.asarray(x, X_test_soft_mosaic.dtype)
###

## 本物、ガウシアンなし、ガウシアンあり
fig = plt.figure(figsize=(14,14))
for i in range(48):
    for j, target in enumerate([X_test, X_test_mosaic, X_test_soft_mosaic]):
        ax = fig.add_subplot(12, 12, i*3+j+1)
        ax.imshow(target[i])
        ax.axis("off")



