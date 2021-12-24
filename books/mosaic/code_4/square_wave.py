import numpy as np
from matplotlib import pyplot as plt


x = np.arange(0, 10, 0.05)
# 50% 矩形波
y = (np.floor(x) % 2 == 0) * 2 - 1
plt.plot(x, y)
plt.savefig('./square_wave.png')
