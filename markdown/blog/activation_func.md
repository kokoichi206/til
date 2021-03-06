この記事は、

> ディープラーニングの学習コードを書いたことはあるが、なぜ活性化関数が必要なのかよく分からない人

を対象としています。

## 概要
```
この記事で取り扱うこと
- 活性化関数が必要な理由
- なぜ非線形でないといけないのかの説明

取り扱わないこと
- ニューラルネットワーク(NN)のモデルの説明
- 活性化関数の具体的な形式
```

### 結論
時間がない人のために先に結論を述べておきます。

```
中間層における活性化関数の持つ非線形性により、
モデルがスケールを獲得し表現力が豊かになるため
```


## 活性化関数の必要性

### ニューラルネットワーク
ニューラルネットワークは、脳内の構造を数学的に模したもので、多層のノード $X^{n}$ からなります。

そして、`n+1`番目の層 $X^{n+1}$ は、`n`番目の層 $X^{n}$ の線型結合で書かれ、各成分は次のような関係式で表されます。

$$
X_i^{n+1} = W_{ij}X_j^{n} + b_i
$$

ここで行列 $W_{ij}$ とベクトル $b_i$ は、"いわゆる"重みとバイアスであり、$j$ については和をとっています。

通常はこの線形変換の後に、`ReLU`などの**非線形**な活性化関数を挟むことが多いです。

### 活性化関数がなかったら
なぜ必要かを考えるにあたり、活性化関数がなかったらどうなるかを考えてみます。

活性化関数を挟まずに複数の層を重ねた場合、`n+2`層目は次のようにかけます

$$
\begin{align}
X_i^{n+2} &= W_{ij}^{n+1}X_j^{n+1} + b_i^{n+1}\\
&= W_{ij}^{n+1}(W_{jk}^{n}X_k^{n} + b_k^{n}) + b_i^{n+1} \\
&= W_{ij}^{n+1}W_{jk}^{n}X_k^{n} + (W_{ij}^{n+1}b_k^{n} + b_i^{n+1}) \\
&= W_{ik}^{\prime}X_k^{n+1} + b_i^{\prime}\\
\end{align}
$$

（ここで、j,k については和をとっています）

この結果は、`n+2`層目のベクトルが`n`層目のベクトルの線形変換でかけていることを意味しています。

そしてこれを繰り返すことで、<span style="color:blue">たとえ 100 層の中間層を入れたとしても 1層（単層）の線形変換の効果しか得られない</span>ということになります。

よって、**線形変換のみからなる多層のネットワークにおいては表現力を持たず、常に１層のネットワークと同等**ということがわかりました。

### 1次元で考える
より考えやすくするために、1次元の線形変換

$$
X^{n+1} = aX^{n} + b
$$

を考えてみます（紛らわしいですが $X^{n}$ は *X*の *n* 乗ではなく、級数 *X* の *n* 番目という意味で使ってます）。

この変換を2回行ったとき、

$$
\begin{align}
X^{n+2} &= aX^{n+1} + b \\
&= a(aX^{n} + b) + b \\
&= aaX^{n} + (ab + b) \\
\end{align}
$$

とかけます。ここで、

$$
a^{\prime} = aa \\
b^{\prime} = ab \\
$$

とおけば、

$$
X^{n+2} = a^{\prime}X^{n} + b^{\prime}
$$

となり、`n+2`層目は`n`層目の線形変換でかけることがわかります。つまり、`n+1`層目が不要ということを意味しており、繰り返すことで全ての中間層が無意味になってしまいます。

### 結論
線形変換のみからなる多層のネットワークにおいては、常に１層のネットワークと同等の効果しか持たず、層を積み重ねる意味がなくなってしまう。

そこで、各線形変換の後に**非線形変換**である活性化関数を挟むことで、表現力を豊かにしてスケールを獲得することになります。


## おわりに
機械学習をやっていると「経験的にこのパラメータを設定する」ということも多いですが、きちんと理論的に考えられる部分も当然あります。そういった部分をきちんと理解していけるようになりたいと思っています。
