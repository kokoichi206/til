## sec 3
ベルマン方程式

エージェントの行動が確率的な振る舞いをする場合の価値関数を求めることが目標

### ベルマン方程式
$$G_t=R_t+\gamma R_{t+1}+\gamma^2R_{t+2}+...\\
=R_t+\gamma (R_{t+1}+\gamma R_{t+2}+...)\\
=R_t+\gamma G_{t+1}$$

収益である、$G_t$と$G_{t+1}$の関係が導かれた！

収益の期待値である状態価値関数は、

$$
v_\pi=\mathbb{E}[G_t|S_t=s]\\
=\mathbb{E}[R_t+\gamma G_{t+1}|S_t=s]\\
=\mathbb{E}[R_t|S_t=s]+\mathbb{E}[G_{t+1}|S_t=s]\\
$$

丁寧に計算を追っていくと、次の**ベルマン方程式**を得る

$$
v_\pi=\sum_{a,s'}\pi(a|s)p(s'|s,a)\{r(s,a,s')+\gamma v_\pi(s')\}
$$

これは、「状態$s$の価値関数」と「その次にとり得る状態$s'$の価値関数」との関係性を表した式である。このベルマン方程式は、全ての状態$s$と全ての方策$\pi$について成り立つ。

### ベルマン方程式の意義
ベルマン方程式によって、無限に続く計算ー手に負えない計算ーを、有限の連立方程式に変換する例をみた。今回のように、ランダムな振る舞いがあったとしても、ベルマン方程式を使えば、その価値関数を求めることができる。

### Q関数とベルマン方程式
$$q_\pi(s,a)=\mathbb{E_\pi}[G_t|S_t=s,A_t=a]$$
Q関数は、状態$s$で行動$a$を行い、そのあとは方策$\pi$に従って行動する。その場合に得られる収益の期待値がQ関数である。

> $q_\pi(s,a)$の行動$a$は、方策$\pi$とは関係ない。$q_\pi(s,a)$の行動$a$は自由に決めることができ、その行動の後は、方策$\pi$にしたがって行動する。

**Q関数のベルマン方程式**

$$
q_\pi(s,a)=\\
\sum_{s'}p(s'|s,a)\{r(s,a,s')+\gamma\sum_{a'}\pi(a'|s')q_\pi(s'|a')\}
$$

### ベルマン最適方程式
ベルマン方程式は、ある方策$\pi$に対してなりたいつ方程式である。ただし、今求めたいのは最適方策であり、最適方策に関しては、ベルマン最適方程式が成立する！

$$
v_\pi(s)=\sum_a\pi(a|s)\sum_{s'}p(s'|s,a)\{r(s,a,s')+\gamma v_\pi(s')\}
$$

最適方策$\pi_*$については、決定論的な最適方策が必ず存在する。決定論的な方策とは、ある状態では常にある特定の行動を選ぶ方策のこと。つまり、ある状態においてある行動を選ぶ確率が１であり、それ以外の行動を選ぶ確率は０ということ。
そのためベルマン方程式では $a$ に関する和をとっているが、その中で計算に関与してくるのは１つの行動だけである。
よって、最適方策に対する**ベルマン最適方程式**は、次のように表される

$$
v_*(s)=\max_a\sum_{s'}p(s'|s,a)\{r(s,a,s')+\gamma v_\pi(s')\}
$$

#### Q関数におけるベルマン最適方程式
行動価値関数（Q関数）においても、同様にベルマン最適方程式を求めることができる

$$
q_*(s,a)=\\
\sum_{s'}p(s'|s,a)\{r(s,a,s')+\gamma\max_{a'}q_*(s'|a')\}
$$

最適方策

$$
\pi_{*}(s)=\argmax_{a}q_{*}(s,a)\\
=\argmax_{a}\sum_{s'}p(s'|s,a)\{r(s,a,s')+\gamma v_{*}(s')\}
$$


## sec 4 動的計画法
Dynamic Programming: DP
動的計画法を使えば、状態と行動の数がある程度大きくなっても価値観数を評価することができる。

### 方策評価
強化学習の問題は、多くの場合２つのタスクに取り組むことになる。方策評価と方策制御。
方策評価というのは、ある方策$\pi$が与えられた時に、その方策の価値関数$v_{\pi}(s)$や$q_{\pi}(s)$を求めること。

> 動的計画法（DP）は、CSの世界ではアルゴリズムの総称として扱われます。 その場合のDPは、対象とする問題を小さな問題に分割して答えを求める手法一般を指す。重要な点は「小さな問題」が繰り返し出現した場合に、それを重複して解かないように——冗長な計算を省くように——工夫すること。その実現方法には、「トップダウン方式（メモ化）」と「ボトムアップ方式」がある。先ほど説明した V_0(s) 、 V_1(s) 、…とひとつずつ繰り上げながら価値関数を更新する手法は「ボトムアップ方式」と呼ばれる


### defaultdict
``` python
from collections import defaultdict  # defaultdictをインポート
from common.gridworld import GridWorld

env = GridWorld()
V = defaultdict(lambda: 0)

state = (1, 2)
print(V[state])  # 0 
# ディクショナリに存在しないキーにアクセスしたとき、
# デフォルト値が設定されたキーが自動で作られる
```

defaultdict を使って、ランダムな方策を定義

``` python
pi = defaultdict(lambda: {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25})

state = (0, 1)
print(pi[state])  # {0:0.25, 1:0.25, 2:0.25, 3:0.25}
```

### 方策反復法
最適な方策を得ることが目標であり、そのための一つの方法は、最適ベルマン方程式を満たす連立方程式を解くこと。しかしその方法では、状態のサイズをS、行動のサイズをAとした時、解を求めるために$S^A$のオーダーの計算量が必要とな理、これは現実的ではない。

そこで、最初のステップとして、現状の方策を正しく評価することが行われる。

次のように、最適ベルマン方程式の右辺を持って、方策$\pi$を更新することを考える

$$
\pi{'}(s)=\argmax_{a}\sum_{s'}p(s'|s,a)\{r(s,a,s')+\gamma v_{\pi}(s')\}
$$

もし$\pi{'}$と$\pi$が等しければ、その$\pi$はすでに最適方策そのもの。

方針が更新された場合、**<span style="color:red">常に</span>方策は改善されることがわかっている！**

より正確には、全ての状態$s$において

$$
v_{\pi{'}}(s)\geq v_{\pi}(s)
$$

が成り立つ（**方策改善定理(Policy Improvement Theorem)**）

#### 評価と改善を繰り返す
価値関数 $v_\pi(s)$に関しては、動的計画法を持って求める

1. $\pi_0$を持って、価値関数$V_0$を評価（DP）
2. $V_0$を使って、greedyに$\pi$を更新（$\pi_1$）
3. $\pi_1$を持って、価値関数$V_1$を評価（DP）
4. $V_1$を使って、greedyに$\pi$を更新（$\pi_1$）
...

以上のアルゴリズムが**方策反復法(Policy Iteration)**

### 方策反復法の実装
遷移が決定論的であり、状態は一意に遷移するものとすると、方策のgreedy化は以下のようになる。

$$
\pi{'}(s)=\argmax_{a}\{r(s,a,s')+\gamma v_{\pi}(s')\}
$$


> greedyな方策は、最大値を取る行動がただ一つ選ばれるので、決定論的な方策です




### 疑問
- 方策の 0.5 で左右に動くっていう方策は変えなくていいんだっけ？
- 辞書の値を「上書き更新」に変えると、元の四季と式と若干変わるのは問題ないのか