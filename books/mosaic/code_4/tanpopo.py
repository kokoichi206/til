!curl -LO http://download.tensorflow.org/example_images/flower_photos.tgz
!tar xzf flower_photos.tgz > /dev/null

!cp flower_photos/dandelion/2294126841_e478564e77_n.jpg flower.jpg


## たんぽぽの高周波の成分と、背景の空の低周波の成分からなる
import matplotlib.pyplot as plt
from PIL import Image

fig = plt.figure(figsize=(8,8))
ax = fig.gca()
ax.imshow(Image.open("flower.jpg"))
ax.axis("off")

## ガウシアンぼかし
import numpy as np
%tensorflow_version 2.x
import tensorflow as tf

img = np.expand_dims(np.asarray(Image.open("flower.jpg"), np.float32), axis=0) / 255.0
kernel_raw = np.array([[1,4,6,4,1], [4,16,24,16,4], [6,24,36,24,6], [4,16,24,16,4],[1,4,6,4,1]], np.float32) / 256.0
out = tf.nn.depthwise_conv2d(img, np.broadcast_to(kernel_raw.reshape(5,5,1,1), (5,5,3,1)), (1,1,1,1), "SAME")
###

fig = plt.figure(figsize=(8,8))
ax = fig.gca()
ax.imshow(out.numpy()[0])
ax.axis("off")


## ガウシアンピラミッドの縮小操作を名前をつけて def
def pyramid_down(inputs):
    kernel_raw = np.array([[1,4,6,4,1], [4,16,24,16,4], [6,24,36,24,6], [4,16,24,16,4],[1,4,6,4,1]], np.float32) / 256.0
    return tf.nn.depthwise_conv2d(img, np.broadcast_to(kernel_raw.reshape(5,5,1,1), (5,5,3,1)), (1,2,2,1), "SAME")
    ###

## 確認用
fig = plt.figure(figsize=(8,8))
ax = fig.gca()
ax.imshow(pyramid_down(img).numpy()[0])
ax.axis("off")

## 拡大側の操作の def
def pyramid_up(inputs):
    kernel_raw = np.array([[1,4,6,4,1], [4,16,24,16,4], [6,24,36,24,6], [4,16,24,16,4],[1,4,6,4,1]], np.float32) / 256.0
    x = tf.image.resize(inputs, (inputs.shape[1]*2, inputs.shape[2]*2), "nearest")
    return tf.nn.depthwise_conv2d(x, np.broadcast_to(kernel_raw.reshape(5,5,1,1), (5,5,3,1)), (1,1,1,1), "SAME")
    ###

## 確認用
out = pyramid_up(gaussian_pyramids[1])
fig = plt.figure(figsize=(8,8))
ax = fig.gca()
ax.imshow(out.numpy()[0])
ax.axis("off")


