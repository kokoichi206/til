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
