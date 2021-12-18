## sec 7 NN と Q学習

チェスの場合、コマの並びパターンは　$10^{123}$ ある！膨大な数を全て経験することは現実的ではない。

Q関数をコンパクトな関数で近似することが、解決策として考えられる。そのための有力な手法が NN！

### DeZero の基礎
- book3 で作った、PyTourch の方言のようなフレームワーク

#### 最適化
ローゼンブロック関数！！
（谷間の形状から真の最小値の検索が難しいことや、その性質から最適化ベンチマーク問題として広く使われている）

$$
y=100(x_1-x_0^2)^2+(x_0-1)^2
$$

の最小値を見つけたい。

>  関数の最小値（もしくは最大値）を取る「関数の引数（入力）」を見つける作業は 最適化 と呼ばれます。ここでの目標は、DeZeroを使って最適化問題を解くことです。

[勾配降下法でローゼンブロック関数](./code/sec_7/gradient_descent_method.png)

学習率の値難しそう、決め方とかある？

### 線形回帰

``` python
import numpy as np

# トイ•データセット
np.random.seed(0)
x = np.random.rand(100, 1)
y = 5 + 2 * x + np.random.rand(100, 1)
```

### Q学習とNN

#### NN の前処理
- カテゴリデータを one-hot ベクトルに変換

``` python
def one_hot(state):
    HEIGHT, WIDTH = 3, 4
    vec = np.zeros(HEIGHT * WIDTH, dtype=np.float32)
    y, x = state
    idx = WIDTH * y + x
    vec[idx] = 1.0
    return vec[np.newaxis, :]  # バッチの次元を追加

state = (2, 0)
x = one_hot(state)

print(x.shape)  # (1, 12)
print(x)  # [[0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0.]]
```

#### Q関数を表すNN
状態 s を input -> NN -> action の数に応じた q 値



