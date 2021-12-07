import numpy as np

np.random.seed(0)

q = 0
for n in range(1, 1111):
    r = np.random.rand()
    q = q + (r - q) / n
    print(q)
