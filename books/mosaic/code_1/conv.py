from PIL import Image, ImageFilter
import matplotlib.pyplot as plt

### 画像を表示する
with Image.open("flower.jpg") as img:
    fig = plt.figure(figsize=(14,14))
    ax = fig.gca()
    ax.imshow(img)

### ガウシアンフィルタ（ぼかし）
with Image.open("flower.jpg") as img:
    img = img.filter(ImageFilter.GaussianBlur())
    ### 
    fig = plt.figure(figsize=(14,14))
    ax = fig.gca()
    ax.imshow(img)

### さまざまなフィルタ
with Image.open("flower.jpg") as img:
    img1 = img.filter(ImageFilter.EMBOSS())
    img2 = img.filter(ImageFilter.CONTOUR())
    img3 = img.filter(ImageFilter.EDGE_ENHANCE())
    img4 = img.filter(ImageFilter.GaussianBlur())
    ### 
    imgs = [img1, img2, img3, img4]

    fig = plt.figure(figsize=(14,10))
    for i, x in enumerate(imgs):
        ax = fig.add_subplot(2,2,i+1)
        ax.imshow(x)


### Convolution
import numpy as np

def conv(inputs, kernel):
    row, column = inputs.shape # 行と列の数
    kr, kc = kernel.shape # カーネルサイズ
    # ここからコードの「None」を置き換えて埋めよ
    outputs = np.zeros((row-kr+1, column-kc+1), inputs.dtype) # 適切なサイズで出力を初期化せよ
    for i in range(row-kr+1): # ループ回数に適切な値を入れよ
        for j in range(column-kc+1): # ループ回数に適切な値を入れよ
            patch = inputs[i:i+row-kr+1, j:j+column-kc+1] # パッチの切り出しを行え
            prod = patch * kernel # パッチ×カーネルを行え
            sum = np.sum(prod) # prodの合計を取れ
            outputs[i][j] = sum # 出力に合計を代入せよ
    ###
    return outputs

X = np.arange(25, dtype=np.float32).reshape(5, 5)
kernel = np.arange(9, dtype=np.float32).reshape(3, 3)
conv(X, kernel)


### 色々なカーネルで畳こむ
X = np.arange(25, dtype=np.float32).reshape(5, 5)

idxs = [0, 1, 3, 4]
for idx in idxs:
    kernel = (np.arange(9).reshape(3, 3) == idx).astype(np.float32)
    print(conv(X, kernel))
##

### PIL の畳み込みを使う
### img.filter(ImageFilter.Kernel(size, kernel, scale, offset))
with Image.open("flower.jpg") as img:
    ### ここにコードを入れる
    img = img.filter(ImageFilter.Kernel((3, 3), (-1,-1,-1,-1,8,-1,-1,-1,-1), 1, 255))
    ### 
    fig = plt.figure(figsize=(14,14))
    ax = fig.gca()
    ax.imshow(img)


### =============== conv tensorflow ===============
# 画像の読み込み：tf.io.decode_jpeg(tf.io.read_file(ファイル名))
# %tensorflow_version 2.x
# import tensorflow as tf
img = tf.io.decode_jpeg(tf.io.read_file("flower.jpg"))
###
print(img.shape)
## 縦解像度、横解像度、カラーチャンネルである（縦と横の順番に注意すること！）
## これは3階テンソルなので4階テンソルに変更する必要がある。具体的には、1番目に軸を付け足す必要がある。
## tf.expand_dims(inputs, axis=軸を増やしたい場所のインデックス)
img = tf.expand_dims(img, axis=0)
###
print(img.shape)

### === 4 次元のカーネル ===
import numpy as np
kernel = np.array([-0.5, -0.5, -0.5, -0.5, 5, -0.5, -0.5, -0.5, -0.5]).reshape(3, 3, 1, 1)
###
kernel = kernel.astype(np.float32)
print(kernel.shape)
print(kernel)

### tf.nn.conv2dを使い、画像：imgをカーネル:kernelによるエッジ強調フィルターを適用せよ。
### ただし、チャンネル単位で畳み込みをすること（重要）
### tf.nn.conv2d(画像のテンソル, カーネルのテンソル, strides, padding)
outputs = []
float_img = tf.cast(img, tf.float32) / 255.0 # uint8 -> floatへのキャスト、[0, 255] -> [0, 1]への変換
### Noneを埋めよ
# print(float_img[0][0][0])
for i in range(len(float_img[0][0][0])):
    conv_result = tf.nn.conv2d(float_img[:,:,:,i:i+1], kernel, 1, "SAME")   # same padding
    outputs.append(conv_result)
###
outputs = tf.concat(outputs, axis=-1) # (1, H, W, 1) -> (1, H, W, 3)に結合

fig = plt.figure(figsize=(14,14))
ax = fig.gca()
ax.imshow(outputs[0].numpy())

### ========== エンボスフィルター ==========
emboss_kernel = np.array([-1, 0, 0, 0, 1, 0, 0, 0, 0]).reshape(3,3,1,1)
emboss_kernel = np.broadcast_to(emboss_kernel, (3,3,3,1))
###
emboss_kernel = emboss_kernel.astype(np.float32)
print(emboss_kernel.shape)
print(emboss_kernel)

### ここにコードを入力
outputs = tf.nn.depthwise_conv2d(float_img, emboss_kernel, strides=[1,1,1,1], padding="SAME")
### 0.5 を足すのを忘れない。。。
outputs = outputs + 0.5
###

fig = plt.figure(figsize=(14,14))
ax = fig.gca()
ax.imshow(outputs[0].numpy())


### Conv2D で、マスク行列を使った方法
# 等高線フィルターのカーネル
contour_kernel = np.array([-1,-1,-1,-1,8,-1,-1,-1,-1]).reshape(3,3,1,1).astype(np.float32) # どうreshapeすればよいか？
contour_kernel = np.broadcast_to(contour_kernel, (3,3,3,3)) # broadcastのshapeはどうすべきか？
# チャンネル単位のマスク
mask = np.eye(3).reshape(1,1,3,3).astype(np.float32) # 3x3の単位行列を生成するにはどうすべきか？
# マスクとかける
# 　注意：[1,1,3,3]とcontour_kernelはshapeが異なるので本来は計算できないが、shape[i]=1の場合に限り、
#　 計算相手のshapeになるまで値が自動的にコピーされる。これをブロードキャストという(broadcast_toのbroadcastはこれ)
contour_kernel = contour_kernel * mask 
# 畳み込み
outputs = tf.nn.conv2d(float_img, contour_kernel, 1, padding="SAME") # conv2dの引数とは？
# オフセット
outputs += 1 # オフセットを入れよ
###

fig = plt.figure(figsize=(14,14))
ax = fig.gca()
ax.imshow(outputs[0].numpy())

