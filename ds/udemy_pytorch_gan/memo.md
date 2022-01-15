## GANs
- GANsは教師なしに属する
    - 生成モデリング

## 数学
- GANs では確率変数が生成されるターゲット
- データが従う確率分布 p そのものはわからないので、生成器の確率分布で近似する
    - 学習では、確率分布を近づけることとなる
- pGをprに近づけるための指標として、KL divergence と JS divergence

![](imgs/divergence.png)

![](imgs/gan_loss.png)

![](imgs/expectation.png)

### Binary Cross Entropy
![](imgs/binary_cross_entropy.png)

なぜ、これで実装するのか


## 実装方針

### 生成器
![](imgs/generator.png)

入力の次元は別に１００じゃなくても良い

#### 転置畳み込み層
![](imgs/transpose_conv.png)

画素値をカーネルで重みづけて、周りに派生させていく。

### 識別器
![](imgs/disc.png)

複数の畳み込みから構成

誤差をしっかり伝播させたいので、LeakyReLU

### 損失関数
Min-Max GAN: 

![](imgs/loss_func.png)


## Conditional GAN
COnditional GAN は、ノイズや画像にラベルを付与することで、特定の画像を生成することができる！

100次元のノイズ＋One hot vector 10次元（ここでは、0-9 の数字の分類に使うので、10次元の One hot vector）

画像に対してラベルを付与する場合は、チャネル方向に追加する。
モノクロに対しては、1次元＋10次元 ⇨ １１チャネルになる

## GANs の課題

### 安定した訓練や判断が難しい
- 生成器と識別器のバランスが崩れるとうまく学習できない
    - 識別器が強すぎる場合には生成器が騙せなくなり、勾配消失が起こる
- モード崩壊
    - 騙しやすい画像が見つかるとそればかり生成するようになり、多様性がなくなる
- 訓練をやめるタイミング
    - 損失関数の値と画像のクオリティが必ずしも相関してない ⇨ いつ訓練を止めるべきか
    - 識別器も更新されていくため

### 訓練プロセスの課題
- モデルを変えると安定して訓練できない
    - DCGAN, Batch Normalization 有無とか

### Wasserstein GAN: WGAN
訓練の安定か/判断を解決するために、Wasserstein-GANが提案された

![](imgs/wasserstein_gan.png)

#### 1-Lipscitz 連続を課す２つの方法
1. Weight Clipping
    * Weight をある値の範囲(-c,c)でクリップする
    * クリップ範囲 c をうまく決める必要がある
1. Gradient Penalty
    * 勾配が１になるような正則化項を追加する

![](imgs/gradient_penalty.png)

#### それ以外の訓練場の工夫
- 生成器と識別器の訓練回数を 1:n_critic にして識別器を多く訓練する
- オプティマイザに RMSProp を使う
- 論文では n_critic に５を与えている
- 生成器の誤差逆伝播は識別器を通って伝搬
    - 識別器が未熟だと真偽の判断がいい加減になるので、上手くフィードバックされない

#### WGAN のメリット
- 損失関数と画像のクオリティの相関があり、解釈がしやすい
- 訓練プロセスが安定する
- モデルや訓練画像の変化に対してロバスト

#### GP: Gradient Penalty
BN は当てないほうがいい。

そもそも、Discriminator の１層目は、なんで最初から BN False にしてたんだっけ？

### Gradient Penalty Loss
``` python
def gradient_penalty(real_imgs, fake_imgs, gp_weight, netD, device):
    batch_size = real_imgs.size()[0]
    alpha = torch.rand(batch_size, 1, 1, 1)
    alpha = alpha.expand_as(real_imgs).to(device)
    fake_imgs = fake_imgs.to(device)
    interpolated_imgs = (alpha * real_imgs.data + (1 - alpha) * fake_imgs.data).requires_grad_()
    interpolated_out = netD(interpolated_imgs)
    grad_outputs = torch.ones(interpolated_out.size()).to(device)
    gradients = torch.autograd.grad(interpolated_out, interpolated_imgs,
                                    grad_outputs=grad_outputs,
                                    create_graph=True, retain_graph=True)[0]
    gradients = gradients.view(batch_size, -1)
    eps = 1e-12
    gradient_norm = torch.sqrt(torch.sum(gradients ** 2, dim=1) + eps)
    gp = gp_weight * ((gradient_norm - 1) ** 2).mean()
    return gp
```

使い方

``` python
lossD_gp = gradient_penalty(real_imgs, fake_imgs, opt.gp_weight, netD, device)
lossD = lossD_real + lossD_fake + lossD_gp
lossD.backward()
optimizerD.step()
```

学習のスピードはゆっくり！
