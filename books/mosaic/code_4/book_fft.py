import numpy as np
import matplotlib.pyplot as plt

sin_x = np.arange(-2*np.pi, 2*np.pi, 0.1)
sin_y = np.sin(sin_x)
###
plt.plot(sin_x, sin_y)

fft_y = np.fft.fft(sin_y)
### 複素数で返ってきた fft_y の絶対値を取る
plt.plot(np.abs(fft_y)[:sin_x.shape[0]//2])


## のこぎり波
saw_x = np.arange(-2*np.pi, 2*np.pi, 0.02)
saw_y = np.zeros(saw_x.shape)
for i in range(1, 201):
    saw_y += np.sin(i*saw_x) / i
###

plt.plot(saw_x, saw_y) 

fft_saw = np.fft.fft(saw_y)
plt.plot(np.abs(fft_saw)[:saw_x.shape[0]//2])
###


# 和の近似のとる部分の個数を変更
fig = plt.figure(figsize=(8,8))
### Noneを埋めよ
for i, k in enumerate([5, 10, 20, 50]):
    ax = fig.add_subplot(2, 2, i+1)
    tmp = np.zeros(saw_x.shape)
    for j in range(1, k+1):
        tmp += np.sin(j*saw_x) / j
    ax.plot(saw_x, tmp)
    ax.set_title("k = "+str(k))
### 加算する次数を減らすとだんだんのこぎりが波打ってくる


## ローパスの実装
fig = plt.figure(figsize=(8,8))
for i, n in enumerate([10, 20, 40, 100]):
    ax = fig.add_subplot(2, 2, i+1)
    flag = (np.arange(saw_x.shape[0]) <= n).astype(np.float32)
    fft_lowpass = fft_saw * flag
    tmp = np.fft.ifft(fft_lowpass)
    ax.plot(saw_x, tmp.real)
    ax.set_title("N = "+str(n))
###


## バンドパスの実装
fig = plt.figure(figsize=(8,8))
thresholds = [0, 10, 20, 40, 100]
for i in range(len(thresholds)-1):
    ax = fig.add_subplot(2, 2, i+1)
    indices = np.arange(saw_x.shape[0])
    flag = ((indices >= thresholds[i]) * (indices <= thresholds[i+1])).astype(np.float32)
    fft_bandpass = fft_saw * flag
    tmp = np.fft.ifft(fft_bandpass)
    ax.plot(saw_x, tmp.real)
    ax.set_title(str(thresholds[i]) + str(" <= N <= ") + str(thresholds[i+1]))
###



## =============== 2dim fft ===============
!curl -LO http://download.tensorflow.org/example_images/flower_photos.tgz
!tar xzf flower_photos.tgz > /dev/null
!cp flower_photos/dandelion/2294126841_e478564e77_n.jpg flower.jpg

## グレースケール化はimgというPILインスタンスに対し、img.convert("L")とすることで実行できる。
from PIL import Image
### flower.jpgを読み込みグレースケール化し、[0, 1]スケールのfloat32型のNumpy配列として定義
with Image.open("flower.jpg") as img:
    img = img.convert("L")
    flower_original = np.asarray(img, np.float32) / 255.0
###
print(flower_original.shape)


fft_image = np.fft.fft2(image)
fft_image = np.fft.fftshift(fft_image)

flower_fft = np.fft.fft2(flower_original)
## 中心が (0,0) となるように shift している
flower_fft = np.fft.fftshift(flower_fft)
fft_plot = np.abs(flower_fft)
###

plt.imshow(flower_original, cmap="gray")
plt.show()
plt.imshow(np.log(fft_plot), cmap="gray")

flower_inv = np.fft.ifftshift(flower_fft)
flower_inv = np.fft.ifft2(flower_inv)
###

plt.imshow(flower_inv.real, cmap="gray")


## 二次元ローパス
from PIL import ImageDraw

def get_circle_mask(radius):
    with Image.new("L", (flower_original.shape[1], flower_original.shape[0]), color=0) as mask:
        draw = ImageDraw.Draw(mask)
        center = np.asarray(flower_original.shape[::-1]) // 2 # (H, W) -> (W, H)
        draw.ellipse((*(center-radius), *(center+radius)), fill=255)
        return np.asarray(mask, np.float32) / 255.0
###

## 確認用
out = get_circle_mask(80)
plt.imshow(out, cmap="gray")


## 二次元ローパス、さまざまな周波数に対して
flower_fft = np.fft.fft2(flower_original)
flower_fft = np.fft.fftshift(flower_fft)
fig = plt.figure(figsize=(10, 10))
for i, r in enumerate([10, 20, 50, 100]):
    mask = get_circle_mask(r)
    out = mask * flower_fft
    out = np.fft.ifftshift(out)
    out = np.fft.ifft2(out)
###
    ax = fig.add_subplot(2, 2, i+1)
    ax.imshow(out.real, cmap="gray")
    ax.set_title("R = "+str(r))



## 二次元バンドパスフィルター
flower_fft = np.fft.fft2(flower_original)
flower_fft = np.fft.fftshift(flower_fft)
fig = plt.figure(figsize=(10, 10))
bradius = [0, 10, 20, 50, 100]
for i in range(len(bradius)-1):
    mask = (1-get_circle_mask(bradius[i])) * get_circle_mask(bradius[i+1])
    out = mask * flower_fft
    out = np.fft.ifftshift(out)
    out = np.fft.ifft2(out)
###
    ax = fig.add_subplot(2, 2, i+1)
    ax.imshow(out.real, cmap="gray")
    ax.set_title(str(bradius[i])+" <= R <= "+str(bradius[i+1]))


## 入力画像 inputs を周波数ごとに分解しプロットする関数
def freq_plot(inputs, fig):
    titles = ["R <= 10", "10 <= R <= 20", "20 <= R <= 50", "R >= 50"]
    def plot_fft(masked_fft, index):
        x = np.fft.ifft2(np.fft.ifftshift(masked_fft)) # masked_fftをスペクトルから画像に戻すこと
        ax = fig.add_subplot(2, 2, index+1)
        ax.imshow(x.real, cmap="gray")
        ax.set_title(titles[index])

    inputs_fft = np.fft.fftshift(np.fft.fft2(inputs))
    # ローパスフィルター
    x = inputs_fft * get_circle_mask(10)
    plot_fft(x, 0)
    # バンドパスフィルター
    x = inputs_fft * (1.0-get_circle_mask(10)) * get_circle_mask(20)
    plot_fft(x, 1)
    x = inputs_fft * (1.0-get_circle_mask(20)) * get_circle_mask(50)
    plot_fft(x, 2)
    # ハイパスフィルター
    x = inputs_fft * (1.0-get_circle_mask(50))
    plot_fft(x, 3)
###

## 確認用
fig = plt.figure(figsize=(10, 10))
freq_plot(flower_original, fig)
