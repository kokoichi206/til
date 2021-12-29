## sec 8
Gated Conv

Contextual Attention ベースのモザイク除去

### Patch Match
Inpainting 独自のアルゴリズム。「マスクされている場所は、マスクされていない場所からのコピペである程度復元できるよね」という発想

Patch Match の発想を NN のモジュールに落とし込んだものが Contextual Attention

### Contextual Attention
1. Deconvolution による画像合成
2. Attention の考え方
3. 画像のパッチ分解


### Deconvolution レイヤー
conv2d の逆変換

``` python
import numpy as np
import tensorflow as tf

x = np.arange(9, dtype=np.float32).reshape(1, 3, 3, 1)
k = np.arange(9, dtype=np.float32).reshape(3, 3, 1, 1)
y = tf.nn.conv2d(x, k, strides=1, padding="VALID")
print(y)
# y/y はスケール調整、Conv2DTransposeの入力が１となるようにする
z = tf.nn.conv2d_transpose(y/y, k, (1,3,3,1), strides=1, padding="VALID")
print(z[0,:,:,0])   # z:(1,3,3,1)
```

一般的には**アップサンプリング層**として使われる。

> CNN では Deconvolution をアップサンプリングとして使うことが多い

### パッチ分解

#### ベクトルのパッチ分解
``` python
x = np.arange(9)
print(x)
print(x.reshape(3, 3))
```

#### 行列のパッチ分解
``` python
x = np.arange(36).reshape(6, 6)
print(x)
# 2*2 のパッチに分解
x = np.reshape(3, 2, 3, 2)
x = np.transpose(x, [0, 2, 1, 3]) # (3,3,2,2)
print(x)
```

### モーションフィルタ
畳み込みフィルターの一種。単位行列をスケーリングしたものがカーネル。各ピクセルを右下方向に１ピクセルずつずらしながらブレンドしたような形になっている

``` python
kernel = np.eye(3, dtype=np.float32).reshape(3,3,1,1) / 3 # motion filter
kernel = kernel * np.elye(3, dtype=np.float32) # channel 単位の畳み込みのため

once = tf.nn.conv2d(orig, kernel, strides=1, padding="SAME")
x = tf.transpose(once, (0, 2, 1, 3))
x = tf.nn.conv2d(x, kernel, strides=1, padding="SAME")
twice = tf.transpose(x, (0, 2, 1, 3))
```

### Contextual Attention
画像のパッチ分解、モーションフィルターのようなぼかし、ソフトマックスによる０−１化、Deconvolutionによるコピペ

### Gated Conv
Contextual Attention をベースに、P-Conv のようなマスク除去のアプローチを取り込んだもの。

### 演習１
```
TensorFlow 2.0.0+GPU
```

#### 色相環
* HSV色空間で画像を定義する。HSV色空間→RGB色空間へはtf.image.hsv_to_rgbで変換可能
* HSV色空間で色相環は
    * H : 色相。円周角を0～1で表す。ラジアン単位で円周角を求め、0～1スケールにすればよい
    * S : 円の中心からの距離を0～1で表す
    * V : 全て1
* ただし円の外側は全ての値は0とする。実装的にはHSVのSが1より大きければ0とすれば良い。

#### 花の画像を割り当てる
全パッチの画像に対するピクセル単位のユークリッド距離が最小の画像を選ぶ


