## sec 7
Generative Adversarial Network

### GAN とは
2014 に生み出された技術で、２つのネットワークを敵対的に（Adversarialに）訓練させていくことで、本物と見分けがつかないようなデータを生成していくネットワークである。

**良質なデータがあり計算資源を惜しまなければ**、本物と見分けがつかない画像生成が可能になっている。

GANとは２つのネットワークからなる。画像を生成する**Generator(G)**、画像が生成されたものか本物かを見分ける**Discriminator(D)**の２つ。

**GとDを相互にかつ敵対的に訓練していく！**

GANの場合は、損失関数$L(G,D)$に対し、

$$
\min_G \max_D L(G, D)
$$

という**min-max**問題を解くものである。

> GANではDとGという２つのネットワークをmin-max問題で訓練する

### GANの考え方
騙し合いの関係にある。損失関数に現れており、

$$
\min_G \max_D L(G, D) = E_{x\sim p_{data}(x)}[\log D(x)] + E_{z\sim p_{z}(z)}[\log (1 - D(z))]
$$

### DCGAN
ノイズを入力し画像を出力する Unconditional GAN の最も基本的なモデル

### GAN の考え方 〜画像を鍛える〜
Image to image translation の GAN には「画像を鍛える」という側面がある。Non-GAN の Image to image translation でもこれは当てはまるが、GANの方がより意識しやすい。具体的には、pix2pixも Cycle GAN で、より広く家が画像を入力するような Conditional GAN を指す。

- 入力がノイズでないGANをConditional GANといい、入力画像に対する条件付き分布となる。
- DCGANというノイズから生成するGANをUnconditional GANという。

GANをマルチステージにして、人間にとって意味のあるような画像を経由するように訓練する手法もある。

### DCGANの訓練ループ
書けるようになろう

### Hinge Loss
GANにおけるAdcersarial Lossはいくつかある。DCGANのような古典的なGANでは、２値分類の交差エントロピーがロスに使われていたが、最近の研究ではHinge Lossの方がいいことがわかっている。Big GANではAdversarial LossにHinge Lossを用いている。

``` python
# 交差エントロピー
def crossentropy_loss(logits, loss_type):
    assert loss_type in ["gen", "dis_real", "dis_fake"]
    reduce_axis = list(range(logits.ndim))[1:]
    if loss_type in ["gen", "dis_real"]:
        val = tf.nn.sigmoid_cross_entropy_with_logits(tf.ones_like(logits), logits)
    else:
        val = tf.nn.sigmoid_cross_entropy_with_logits(tf.zeros_like(logits), logits)
    return tf.reduce_mean(val, axis=reduce_axis)
```

入力は成果負荷の確率（0~1）ではなく**ロジット（-∞〜∞）**となる。ロジットにシグモイド関数を適応すると確率に変形できる。

いくら出力ロジットが大きくなってもロスが永遠に０にならず、無限に強化されるということが起こる。

交差エントロピーのように、本物・偽物の差を無限に広げるというよりも、「出力層において本物と偽物が一定の差を取るように最適化する」と考えた方が良い。この発想を取り入れたものがHinge Loss。

``` python
# Hinge Loss の実装
def hinge_loss(logits, loss_type):
    assert loss_type in ["gen", "dis_real", "dis_fake"]
    reduce_axis = list(range(logits.ndim))[1:]
    if loss_type == "gen":
        return -tf.reduce_mean(logits, axis=reduce_axis)
    elif loss_type == "dis_real":
        minval = tf.minimum(logits - 1, tf.zeros(logits.shape, dtype=logits.dtype))
        return -tf.reduce_mean(minval, axis=reduce_axis)
        val = tf.nn.sigmoid_cross_entropy_with_logits(tf.ones_like(logits), logits)
    else:
        minval = tf.minimum(-logits - 1, tf.zeros(logits.shape, dtype=logits.dtype))
        return -tf.reduce_mean(val, axis=reduce_axis)
```

上記Hinge lossではDが無限に強化されるということは怒らない。

弱い損失関数を用いるという視点は、GANの安定化と関連している。弱い損失関数を使い連続性を保証するほど、GANの 安定性が向上し、出力の画質が向上するとされている

### GANの問題点

#### 勾配の消失
DとGを交互に学習させることによって発生する。教師あり学習ではResNetなどなどネットワークの工夫次第ではほぼ消失しないが、GANではいくら工夫しても起こることがある。例えば、Dが強くなりすぎてGが騙せなくなったケースなどでは、勾配が消失してると言える。

#### モード崩壊
いかなる入力に対しても同一画像を出力するもの。Gがダマスことに成功しすぎてDが見分けられなくなってしまい、Gが似たような画像ばかり生成するようになるもの。

#### Image to image の際
この時はあんまり気にならないかも？Image to imageにおいてはAdversarial Lossを単独で使うことは少なく、

$$
L = L_{adv} + \lambda L_1
$$

のようにL1ロストミックスして使うことが多い。L1ロスがGANの安定性を向上させているという側面もある。

### GANの向き不向き

#### とりあえずNon-GANで訓練してみる

#### Non-GANでこれは嘘っぽい、本物っぽいと考え出したらGANを検討する

#### Non-GANの損失関数のチューニング沼にもGANは向いている
GANには動的な損失関数という側面もあるので、L1ロスのような定番の損失関数を使いながらも、残りをAdversarial Lossで調整するという方法もある。まさにこれがpx2pixである。


### リプシッツ定数とGANの安定性
**Dのリプシッツ連続やリプシッツていすつのコントロールが重要**

GANの生成画像をきれいにするには、最適化したいパラメーター$\theta$とモデルの出力$P(\theta)$のマッピングがより滑らかである方が良い。この時、「連続」という概念が重要となる。連続性を確保するために、Dのモデルや損失関数に**1-リプシッツ連続**という強い制約を置いたのがWGANである

リプシッツ連続の定義

$$
\frac{d_Y(f(x_1), f(x_2))}{d_X(x_1, x_2)} \le K \quad (\forall x_1, x_2 \in X)
$$

ここに対し、$K=1$という制約を置くのがGANの安定性を向上させる上で有効である。**K**をリプしっつ定数という。

> リプシッツ定数とは関数の連続性を示すパラメーター。GANの安定性と密接な関係がある。

### Spectral Normalization
GANの連続性は、Batch Normalizationで損なわれがち。そこで、Normaliztionを連続になるように置き換えたもの。

特異値分解（Singular Value Decomposition:SVD）

ただ、特異値分解は計算量が大きいため、Power Iterationというアルゴリズムを使って高速に計算させている。

Spectral Normalizationとは、係数の最大特異値でNormalizationすることで、リプシッツ定数をコントロールするものである。これにより、GANのモード崩壊や勾配消失を起こりにくくする効果がある（WGANやWGAN-GPと似た効果がある）。

### Paired / Unpaired Data
Unpaired というのは、男性の顔を女性の顔に変換したり、実写の顔をアニメ顔に変換したり、簡単にはデータの対応が作れないケース。この場合、ドメイン単位での対応は作れるが、サンプル単位での対応は作らない。

Paired Data に対するGANによるImage to image translation は pix2pix、Unpaired Data では Cycle GAN が最も基本的

### pix2pix
Image to image translation (Conditional GAN) のうち Paired Data に対して使えるモデル。

パンの形の上のスケッチに猫を投影したり、写真の背景を削除したり、スケッチからポケモンを生成（着色）したり。

G の最適化で L1ロスを使っている！

ノイズから生成し、Adversarial Loss だけ用いる DCGAN よりも、pix2pix の方が訓練が安定することが多

### Patch GAN
Image to image translation の D では、画像全体の本物・偽物を見分けるのではなく、画像の小さいパッチ単位の本物・偽物の確率を求める。これが Patch GAN

### Cycle GAN
Unpaired Data に対する Image to image translation のベースライン

馬 → しまうま の変換など

**Cycler GAN では CNN が４つ必要**。

Consistency Loss というロス。Cycle  Consistency Loss とは、**行って戻ってきたら元の画像になるよね**というものである。

背景を対象物体と間違えるなどの失敗報告も多い


### 演習1
SNGAN、BigGANなどSpectral Normalizationを適用したGANのモジュール構成

- Generator : ConvSN2D -> Batch Normalization / Instance Normalization -> ReLU
- Discriminator : ConvSN2D -> ReLU

#### ネットワークの確認
Gは入力・出力ともに64x64x3、Dは入力が64x64x3で出力が8x8x1である

Gはある画像を入力とし、ペアとなる画像を出力とするのでこれでOKである。Dは入力画像が本物であるかどうかを見分けている。

では、Dの出力の「8x8x1」とは？
これは画像のパッチ単位で本物か偽物かを見分けている。もし1枚の画像を本物か偽物かを見分けるのなら、出力は1x1x1となる。8x8x1は何を意味するのかというと、64x64の解像度の画像に対し、8x8サイズのパッチを縦8個、横8個並べ、各々のパッチが本物か偽物かを調べなさいという意味である。もし出力サイズが4x4x1ならパッチサイズは16x16、16x16x1ならパッチサイズは4x4となる。

これはPatch GANと呼ばれ（Spectral Normが入っているので、論文ではSN Patch GANと呼ばれることもある）、Image to image translationでは画像全体の本物・偽物を識別するよりPatch GANのほうが好まれることが多い。

#### Hinge loss
ロジスティクス回帰のシグモイド関数適用前のロジットという位置づけ


$$
y(x) = -x_{fake} \quad (for G) \\
y(x) = -\min(-x_{fake}-1, 0)-\min(x_{real}-1, 0) \quad (for D)
$$

上のモデルにおいては 𝑥 のshapeは(n, 8, 8, 1)となる

### 演習2
pix2pixの演習問題で「無修正画像とモザイク画像が同時に手に入るのはおかしいのではないか」と感じた方もいるかもしれない。この指摘はもっともで、同一の画像について無修正とモザイクが手に入るのは、あたかも答えを知った上で学習しているようで、できて当然ではないかと思うかもしれない。

そのような疑問を持っている方は、おそらくこういう問題設定なら満足するのではないだろうか。「無修正画像が1万枚、モザイク画像が1万枚あり、無修正とモザイクの間で別々の被写体であり、無修正－モザイクの対応がない場合に除去ってできる？」という設定である。



### Links
- [pix2pix](https://arxiv.org/abs/1611.07004)
    - [Github](https://github.com/phillipi/pix2pix)
