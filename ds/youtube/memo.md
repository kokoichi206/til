## numpy
```python
import numpy as np

a = np.array([[0, 1, 2],
              [3, 4, 5]])

print(a.shape)
b = np.array([0, 1, 2, 3, 4, 5, 6, 7])    # 配列の作成
c = b.reshape(2, 4)                       # (2, 4)の2次元配列に変換
print(c)

# reshapeの引数を-1にすることで、どのような形状の配列でも1次元配列に変換することができます。
d = np.array([[[0, 1, 2],
               [3, 4, 5]],
                  
                  [[5, 4, 3],
                   [2, 1, 0]]])  # 3重のリストからNumPyの3次元配列を作る


e = d.reshape(-1)
print(e) # [0 1 2 3 4 5 5 4 3 2 1 0]

a = np.array([[0, 1, 2],
              [3, 4, 5]])  # 2次元配列

print(np.sum(a))  # 15
print(np.average(a))  # 2.5
print(np.max(a))    # 5
print(np.min(a))    # 0

b = np.array([[0, 1, 2],
              [3, 4, 5]])  # 2次元配列

print(np.sum(b, axis=0))  # 縦方向で合計
print(np.sum(b, axis=1))  # 横方向で合計

import numpy as np

b = np.array([[0, 1, 2],
              [3, 4, 5]])  # 2次元配列

print(np.sum(b, axis=0))  # 縦方向で合計, axis=0 方向を走る
print(np.sum(b, axis=1))  # 横方向で合計
# [3 5 7]
# [ 3 12]
```

## neuron
```python
import numpy as np
import matplotlib.pyplot as plt

def neuron(x, w, b):  # x:入力 w:重み b:バイアス
    u = np.sum(x*w) + b
    y = 0 if u < 0 else 1  # ステップ関数
    return y

steps = 20  # 入力を変化させるステップ数
r = 1.0  # 入力を変化させる範囲（-1から1まで）

X1 = np.linspace(-r, r, steps)  # 入力1
X2 = np.linspace(-r, r, steps)  # 入力2
image = np.zeros((steps, steps))  # 出力を格納する2次元配列

w = np.array([-0.5, 0.5])  # 重み
b = 0  # バイアス

for i_1 in range(steps):  # 入力1を変化させる
    for i_2 in range(steps):  # 入力2を変化させる
        x = np.array([X1[i_1], X2[i_2]])  # 入力
        image[i_1, i_2] = neuron(x, w, b)  # 出力を配列に格納

plt.imshow(image, "gray", vmin=0.0, vmax=1.0)  # 配列を画像として表示
plt.colorbar()
plt.xticks([0, steps-1], [-r, r])  # x軸ラベルの表示
plt.yticks([0, steps-1], [-r, r])  # y軸ラベルの表示
plt.show()
```

