!pip install tensorflow==2.0.0

!wget https://www.robots.ox.ac.uk/~vgg/data/flowers/102/102flowers.tgz
!tar -xvzf 102flowers.tgz > /dev/null
!cp jpg/image_00810.jpg flower.jpg


from PIL import Image
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(14, 14))
ax = fig.gca()
ax.imshow(Image.open("flower.jpg"))


import numpy as np
import tensorflow as tf

# 512px にリサイズしたあと、ダウンサンプリング
with Image.open("flower.jpg") as img:
    img = img.resize((512, 512), Image.LANCZOS)
    original = np.asarray(img, np.float32) / 255.0
    original = np.expand_dims(original, axis=0)
    kernel = np.ones((2,2,1,1), dtype=np.float32) / 4.0 * np.eye(3).reshape(1,1,3,3)
    original_half = tf.nn.conv2d(original, kernel, 2, padding="VALID")
    ###

    ## 確認用
    print(original_half.shape)
    fig = plt.figure(figsize=(10,10))
    ax = fig.gca()
    ax.imshow(original_half[0])

# Deconvolution によるアップサンプリング
deconv_up = tf.nn.conv2d_transpose(original_half*4, kernel, output_shape=(1, 512, 512, 3), strides=2, padding="VALID")
###

## 確認用
print(deconv_up.shape)
fig = plt.figure(figsize=(10, 10))
ax = fig.gca()
ax.imshow(deconv_up[0])


# ランダムで９枚選び、全ての組み合わせの合成を行う
import itertools

# 使う画像をランダムで選択
np.random.seed(123)
idx = np.random.randint(0, 8000, (9, ) )
# パッチの格納
patches = np.zeros((128, 128, 3, idx.shape[0]), np.float32)
for i, id in enumerate(idx):
    patches[:,:,:,i] = np.asarray(Image.open(f"jpg/image_{id:05}.jpg").resize((128, 128), Image.LANCZOS), dtype=np.float32)
patches = patches / 255.0

# 9C2の列挙
combine = np.array(list(itertools.combinations(np.arange(9), 2))) # (36, 2)
# パッチを組み合わせる割合。最後の軸がパッチのインデックス
deconv_inputs = (np.expand_dims(combine, axis=-1) == np.arange(9).reshape(1, 1, -1)).astype(np.float32) # (36, 2, 9)
deconv_inputs = np.sum(deconv_inputs, axis=1).reshape(1, 6, 6, 9) / 2

deconv_out = tf.nn.conv2d_transpose(deconv_inputs, patches, output_shape=(1, 768, 768, 3), strides=128, padding="VALID")
###

## 確認用
# パッチのプロット
fig = plt.figure(figsize=(9, 9))
for i in range(idx.shape[0]):
    ax = fig.add_subplot(3, 3, i+1)
    ax.imshow(patches[:,:,:,i])
# Deconvolutionの結果のプロット
fig = plt.figure(figsize=(10, 10))
ax = fig.gca()
ax.imshow(deconv_out[0])



# 色相環
hsv_matrix = np.zeros((64, 64, 3), np.float32)
# xy座標系
coordinates = np.stack(np.meshgrid(np.arange(64), np.arange(64)), axis=-1) - 32 # x, y座標 (64, 64, 3)
coordinates[:,:,1] = coordinates[::-1,:,1] # yの向きが逆なので反転
# xy座標→角度（ラジアン）
rad = np.arctan2(coordinates[:,:,1], coordinates[:,:,0])
rad[rad<0] += np.pi * 2
hsv_matrix[:,:,0] = rad / (2 * np.pi) # H
hsv_matrix[:,:,1] = np.sqrt(np.sum(coordinates**2, axis=-1))/32.0
hsv_matrix[:,:,2] = 1.0
# HSV色空間
hsv_matrix *= (hsv_matrix[:,:,1:2] <= 1.0).astype(np.float32)
# HSV -> RGB
rgb_matrix = tf.image.hsv_to_rgb(hsv_matrix).numpy()

fig = plt.figure(figsize=(8,8))
ax = fig.gca()
ax.imshow(rgb_matrix)

# 距離が最短の画像を選ぶ
import glob

# ランダムに1024枚選択（メモリオーバー対策）
patches = []
paths = sorted(glob.glob("jpg/*.jpg"))
np.random.seed(123)
np.random.shuffle(paths)
for path in paths[:1024]:
    patches.append(np.asarray(Image.open(path).resize((24, 24), Image.LANCZOS), np.float32))
patches = np.array(patches, np.float32) / 255.0 # (1024, 24, 24, 3)

# チャンネル別に距離を計算（メモリ対策）
dists = np.zeros((64, 64, 1024), np.float32)
for i in range(3):
    dists += np.sum((patches[:,:,:,i].reshape(1, 1, patches.shape[0], 24, 24) -
                     rgb_matrix[:,:,i].reshape(64, 64, 1, 1, 1))**2, axis=(3,4))
ratio = (dists == np.min(dists, axis=-1, keepdims=True)).astype(np.float32) # (64, 64, 1024)
ratio = np.expand_dims(ratio, axis=0)

# Deconvでコピペ
result = tf.nn.conv2d_transpose(ratio, patches.transpose((1,2,3,0)), output_shape=(1,64*24,64*24,3), strides=24, padding="VALID")
###

# 結果の表示
fig = plt.figure(figsize=(20,20))
ax = fig.gca()
ax.imshow(result[0])
# ファイルとして保存
x = (result[0].numpy()*255.0).astype(np.uint8)
with Image.fromarray(x) as img:
    img.save("mosaic_hard.jpg", quality=95)

