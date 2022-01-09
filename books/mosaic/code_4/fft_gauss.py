import numpy as np
from math import sqrt, pi, exp
import matplotlib.pyplot as plt


SIZE = 30
fig = plt.figure(figsize=(2*SIZE,SIZE))
FONTSIZE = 60


N = 4096            # サンプル数
s = N/256           # 標準偏差

y = []
for i in range(N):
    x = i - N/2
    v = exp(-x**2/(2.0*s**2))/(sqrt(2*pi)*s)
    y.append(v)

ax = fig.add_subplot(121, xlim=(N/2-100,N/2+100))
# ax = fig.add_subplot(1, 2, 1)
ax.plot(y)
ax.tick_params(axis='x', labelsize=FONTSIZE)
ax.tick_params(axis='y', labelsize=FONTSIZE)
ax.set_xlabel("counts", fontsize=FONTSIZE)
ax.set_ylabel("x", fontsize=FONTSIZE)
ax.set_title("Real Gauss", fontsize=FONTSIZE, fontname='IPAexGothic')
# ax.set_title("Real Gauss", fontsize=FONTSIZE)
# plt.plot(y)
# plt.xlim([N/2-100,N/2+100])
# plt.show()

# fk = np.fft.fft(y)
# plt.plot(fk)

# 配列のインデックスと k の関係
# ## 横軸は点の番号、縦軸は k の値
# ## -1/2 < k < 1/2 となっている
# freq = np.fft.fftfreq(N)
# plt.plot(freq)

freq = np.fft.fftfreq(N)
fk = np.fft.fft(y)
# plt.xlim([-0.05, 0.05])
# plt.scatter(freq, fk, s=1)
# plt.show()

ax = fig.add_subplot(122, title='FFT of Gauss', xlim=(-0.05, 0.05))
# ax = fig.add_subplot(1, 2, 1)
ax.scatter(freq, fk)
ax.tick_params(axis='x', labelsize=FONTSIZE)
ax.tick_params(axis='y', labelsize=FONTSIZE)
ax.set_xlabel("counts", fontsize=FONTSIZE)
ax.set_ylabel("k", fontsize=FONTSIZE)
ax.set_title("FFT of Gauss", fontsize=FONTSIZE, fontname='IPAexGothic')
fig.savefig('./fft_gauss.png')

