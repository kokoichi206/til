## CodeMemo
```python
import numpy as np
a = np.random.randn(5)
expa = np.exp(a)
A = np.random.randn(100, 5)
expA = np.exp(A)
ans = expA / expA.sum()
ans = expA / expA.sum(axis=1, keepdims=True)
```


## softmax
- 確率で考えたいから、負の数嫌だ〜〜 → exp取ろう
- めっちゃ数デカくなっちゃって嫌だ〜〜 → 相対比にしよう


## Training Summary
- Training == finding the "best" weights for the neural network
- "best" weights are the weights that minimize the cost
- Cost == negative log-likelihood of categorical distribution
- Ex. die roll
- Also improves prediction accuracy
- Backpropagation
- Fancy name for gradient descent

Nonlinear classifier

classic examples: XOR and donut

to gain deeper insight

## ANNs for Regression
- Classification is the typical use-case for ANNs
- All famous results were classification problems(MNIST, ImageNet, etc)
- ANNs are better at classification than regression

### How to use ipython
```sh
$ ipython
```
