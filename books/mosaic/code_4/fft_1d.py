import numpy as np
from matplotlib import pyplot as plt


x = np.arange(0, 10, 0.05)
# 50% 矩形波
y = (np.floor(x) % 2 == 0) * 2 - 1
# fk = np.fft.fft(y, n=None, axis=-1, norm=None)
# print(fk)
fk = np.fft.fftfreq(y, n=None, axis=-1, norm=None)
print(fk)

F = np.fft.fft(x) # 変換結果
freq = np.fft.fftfreq(N, d=dt) # 周波数

fig, ax = plt.subplots(nrows=3, sharex=True, figsize=(6,6))
ax[0].plot(F.real, label="Real part")
ax[0].legend()
ax[1].plot(F.imag, label="Imaginary part")
ax[1].legend()
ax[2].plot(freq, label="Frequency")
ax[2].legend()
ax[2].set_xlabel("Number of data")
plt.show()

plt.plot(x, fk)
plt.savefig('./fft_1d.png')