## sec 4
モザイクの科学

画像ピラミッド、フーリエ変換

モザイクとは「**高周波にノイズの乗るローパスフィルター**8」

### 波としての画像
画像の「周波数」に注目する。

音は波の性質を持つ。シンセサイザー。

$$
y = \sin{(x)}
$$

``` python
import numpy as np
x = np.arange(0, 10, 0.01)
y = np.sin(x) # (1000, )
```

$$
z = \sin{(x+y)}
$$

``` python
x = np.arange(0, 10, 0.01)
y = np.arange(0, 10, 0.01)
z = np.sin(x + y) # (1000, 1000)
```

[0, 1] に出力を合わせる

$$
z = \frac{\sin{(x+y)}+1}{2}
$$

並のデータを考えるときには、波を１つの関数と見做して、その関数を複数の sin 関数の合成として捉えるという手法（フーリエ変換）がある。

**音は目的変数がベクトルであったが、目的変数を行列に拡張すれば画像も波として考えることができる**

つまり、画像も sin 波の合成として捉えられ、このアプローチにより「周波数」の概念が出てくる

音において周波数を上げることは音の高さを意味する。

画像における周波数とは。

- 低周波成分：全体のぼやっとした雰囲気、色合い
  - 空や雲
- 高周波成分：細部の輪郭線
  - エッジや髪の毛のような細い線

> 画像の低周波成分とは、全体のぼやっとした雰囲気や色合い、高周波成分とは輪郭線や細い模様をそれぞれ対応

### ガウシアンピラミッド
ラプラシアンピラミッドは、バンドパスフィルターに近い存在として位置付けられる。

ガウシアンピラミッドではカーネルサイズ 5×5 の畳み込みをすることが多い。5×5 の場合カーネルは、

$$
K=\frac{1}{256}
\left(
\begin{array}{ccccc} 
1 & 4 & 6 & 4 & 1\\
4 & 16 & 24 & 16 & 4\\
6 & 24 & 36 & 24 & 6\\
4 & 16 & 24 & 16 & 4\\1 & 4 & 6 & 4 & 1\\
\end{array}
\right)
$$

``` python
x = original_image
results = [x]
for i in range(n):
    x = gaussian_blur(x) # ガウシアンぼかし
    x = downsampling(x) # 1/2 に縮小
    results.append(x)
```

解像度が小さくなるに従い、全体の雰囲気のみが表現されるようになる。
これはガウシアンぼかし＋リサイズにより、次第に高周波の成分が削ぎ落とされ、低周波の部分だけが残るようになったからである。

### ラプラシアンピラミッド
ガウシアンピラミッド同士の差分を取ったもの

ガウシアンぼかしはローパスフィルターの役割がある。

> ラプラシアンピラミッドを使えば、畳み込みとリサイズだけで近似的に周波数特性をみれる

### １次元フーリエ変換
FFTとは高速フーリエ変換の略であるが、単にフーリエ変換のことをFFTということも多い。

逆フーリエは、ifft

### 1d fft

#### 離散フーリエ変換(DFT)
配列のどのインデックスがどの座標に対応してるの？
`numpy.fft.fft`に一次元配列を渡すと、デフォルトでは、インデックス i と、座標 x が等しいものとして計算される。

N個のデータのDFTのデータは、やはりN個になるため、結果は要素N個の一次元配列となる。その順番とkの対応は`numpy.fft.fftfreq`にデータ点数を与えることで得られる。

計算の都合上、f(k) = (-1)^k A_k と、(-1)^k がかかってしまう！


### 2次元フーリエ変換
np.fft.fft2

**境界部分と内側のベタ塗りで周波数が大きく異なる！**

画像では周波数は解像度に対応するので、ほんの小さい領域しか見ない高解像度の畳み込みレイヤーでは、全体の形状を意識しながら画像を生成するのが難しい。

![](imgs/fft_2d_filter.png)

### 画像ピラミッドのDLへの応用
Octave Convolution 少し難しい

### リサイズによる周波数特性
画像では解像度≒周波数なので、**画像を縮小して拡大するという操作は基本的にローパスフィルター**となる。
ただし、リサイズアルゴリズムによって周波数特性はかなり変わる。

- ローパスフィルターによってカットされた高周波成分の回復
- NN 法のようなチープなリサイズアルゴリズムによって乗った、格子状のスペクトルノイズの除去

### ガウシアンぼかしによる周波数特性
ガウシアンローパスフィルター、とも呼ばれる

### L1-loss の問題点
L1ロスはピクセル単位の違いを表現するのに便利な損失関数であるが、パターンや図柄を捉えているかというと、必ずしもそうではない。

このような問題に対し、さまざまな損失関数を足してL1ロスの欠点を補うという方法が考えられる。SP-Loss

損失関数を複数足す方法は古くからあるが、**損失関数のハイパーパラメータ**の調整が大変、という問題がある

$$
L = \alpha L_1 + \beta L_2 + \gamma L_3+\dots
$$

のような、$\alpha,\beta,\gamma$のようなパラメータチューニングがしんどい。**静的な関数では表せないが、その時々で役割が変わり、複数の損失関数をあわせて１つにしたような動的な損失関数**があるといいなぁ。

これを実現したのがGAN（Generative Adversarial Network）で、GANは画像が「本物っぽいかどうか」を判定するメタな損失関数と言える。

> ピクセル単位のL1ロスは必ずしも全体の形状を評価しないため、出力画像がぼやけることが。そのため、画像間の相関や類似度を考えたり、複数の損失関数の合成、GANベースのアプローチが有効

### Perception-Distortion Tradeoff
以下の２つの軸を同時に高めることは**不可能**

- 画像を人間が見て違和感がないかという直感性（Perception）
- L1ロスのようにピクセル間の正確性を高めるという歪み（Distortion）

定量化しやすいのは、やはり歪みの軸で、L1ロスやL2ロスは最もベーシックな指標となる。L2ロスをベースとしているPSNRは最もわかりやすい歪みの指標となる。しかし、PSNRはピクセル間の計算にこだわりすぎる傾向があり、例えば画像を1,2ピクセル平行移動しただけで、大きなマイナスになる。。。

これを補完する形で使われるのが、SSIMやMS-SSIM。

SSIMはPSNRと似た歪みの指標であるが、店ではなく小さいパンチ単位で評価する。

$$
SSIM(x, y) = \frac{(2\mu_x\mu_y+c_1)(2\sigma_{xy}+c_2)}{(\mu_x^2+\mu_y^2+c_1)(\sigma_x^2+\sigma_y^2+c_1)}
$$

SSIMとは画像ノッチさなパッチに対して、平均、分散、共分散を求めて比較することでもとまる。SSIMは -1~1 で表され、1 に近いほど似ている画像とされる。SSIMはパッチ単位で評価しているので微小な平行移動に対してロバストという特徴がある。MS-SSIM は見る解像度を変えて評価するもの。

直感性のスコアはどうやって測定しようか？超解像の Ma et al. スコアなどは参考になるかも

Ma et al. スコアの高いアルゴリズムは「〜〜GAN」というものが多い。失われるトレードオフをうまい具合にチューニングするには、損失関数を以下のように定義

$$
L = L_{GAN} + \lambda L_{L1}
$$



### 演習
ガウシアンピラミッドの縮小操作は、ガウシアンぼかしをかけてからダウンサンプリングをするというものである。TensorFlowのDepthwise Convでは、縦横方向のstrides=2とすれば良い。

#### のこぎり波
三角関数の合成で表される関数で、

$$
f(x) = \sum^{\infty}_{k=1} \frac{1}{k}\sin(kx)
$$

で表される関数である(saw_y)。

``` python
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
```

のこぎり波はシンセサイザーに使われ、のこぎり波をたくさん重ね合わせることでストリングス（弦楽器）の音として用いることができる。


#### ローパス
- データをFFTにかける
  - `np.fft.fft()`
- FFTの結果に対し、最初のN個だけ1をかけ、残りに対しては0をかける（ローパスフィルター）
- ローパスフィルターを適用したFFTに対し、逆フーリエ変換を適用しデータの空間に戻す
  - `np.fft.ifft()`

``` python
fig = plt.figure(figsize=(8,8))
for i, n in enumerate([10, 20, 40, 100]):
    ax = fig.add_subplot(2, 2, i+1)
    flag = (np.arange(saw_x.shape[0]) <= n).astype(np.float32)
    fft_lowpass = fft_saw * flag
    tmp = np.fft.ifft(fft_lowpass)
    ax.plot(saw_x, tmp.real)
    ax.set_title("N = "+str(n))
###
```

#### バンドパス
ローパスの、かけるフィルターが違うのみ

``` python
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
```

#### 画像のフーリエ変換（２次元のフーリエ変換）
`np.fft.fft2(image)`を使う。imageは行列。

画像は3階テンソルであるので、

``` python
out = np.zeros(inputs.shape, dtype=np.complex128)
for i in range(inputs.shape[-1]):
    out[:,:,i] = np.fft.fft2(inputs[:,:,i])
```

のように**カラーチャンネル別にFFTするか、グレースケール画像として事前に変換しておく**必要がある

#### FFT2
fft2dのデフォルトの出力は周波数ゼロが左上にきて見づらい。そこで、ゼロを中央に、外側にいくほど高周波となるように座標変更する。これは、np.fft.fftshitという関数でできる。

```
fft_image = np.fft.fft2(image)
fft_image = np.fft.fftshift(fft_image)
```

``` python
flower_fft = np.fft.fft2(flower_original)
## 中心が (0,0) となるように shift している
flower_fft = np.fft.fftshift(flower_fft)
fft_plot = np.abs(flower_fft)
###

plt.imshow(flower_original, cmap="gray")
plt.show()
plt.imshow(np.log(fft_plot), cmap="gray")
```

``` python
flower_inv = np.fft.ifftshift(flower_fft)
flower_inv = np.fft.ifft2(flower_inv)
###

plt.imshow(flower_inv.real, cmap="gray")
```

#### 二次元ローパス
``` python
from PIL import ImageDraw

def get_circle_mask(radius):
    with Image.new("L", (flower_original.shape[1], flower_original.shape[0]), color=0) as mask:
        draw = ImageDraw.Draw(mask)
        center = np.asarray(flower_original.shape[::-1]) // 2 # (H, W) -> (W, H)
        draw.ellipse((*(center-radius), *(center+radius)), fill=255)
        return np.asarray(mask, np.float32) / 255.0

## 確認用
out = get_circle_mask(80)
plt.imshow(out, cmap="gray")
```

> Rが低くても高くても背景の雲は同じように描画されている。一方で、Rが低いとたんぽぽの綿毛がぼやけて、Rが大きくなるに従って綿毛の輪郭が描画されていく。つまり、雲の部分は低周波成分で、綿毛の部分が高周波成分であることがわかる。

> また別の見方をすれば、Rが低いほどぼやけた画像となる。ガウシアンぼかしやモザイクをかけた画像とは、低周波成分のみ残って高周波成分が消えた画像ということができる。これは特にガウシアンぼかしで成立する。ガウシアンぼかしをガウシアンローパスフィルターと言ったり、単にローパスフィルターというのはこのためである。

#### 二次元バンドパスフィルター
``` python
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
```

- モザイクとは高周波の成分にノイズが乗るローパスフィルタだあ！
- 「モザイク除去」＝「拡大縮小の超解像問題＋ノイズ除去」

