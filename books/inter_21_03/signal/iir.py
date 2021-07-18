import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq, fftshift, rfit, rfftfreq


Fs = 200    # サンプリング周波数

Fh = 0.5
Fl = 30.0
Nf = 1      # ハイパスフィルタ/ローパスフィルタの次数

# バターワース型のフィルタを設計
bh, ah = signal.butter(Nf, Fh, 'high', fs=Fs)
bl, al = signal.butter(Nf, Fl, 'low', fs=Fs)

Fn = 50.0   # のっちフィルタ中心周波数
Q = 4.0
bn, an = signal.iirnotch(Fn, Q, fs=Fs)

AMP_COEF = 5.0 / 2**12 / 1000 * 1000000

plt.rcParams["font.size"] = 16

YLIM = 310
VMAX = 100

CH = 1
DAT_LEN = 100

EYE_CLOSE = 43
EYE_OPEN = 70
SPECRUM_LEN = 2

EEG_FILE_NAME = 'eeg.txt'   # 脳波データファイル

def read_dat(filename):
    dat = np.loadtxt(filename, delimiter='\t')
    dat = dat[0:int(Fs * DAT_LEN), CH] * AMP_COEF
    return dat

def plot_wave(dat, is_wide=True):
    t = np.arange(len(dat)) / Fs
    if is_wide:
        plt.figure(figsize=[11, 4])
    else:
        plt.figure(figsize=[7, 4])

    plt.plot(t, dat)
    plt.ylim(-YLIM, YLIM)
    plt.xlabel('Time [s]')
    plt.ylabel('Ch' + str(CH+1) + ' [uV]')
    plt.show()


if __name__ == "__main__":
    dat = read_dat(EEG_FILE_NAME)

    dat_h = signal.lfilter(bh, ah, dat) # ハイパスフィルタ適用
    dat_l = signal.lfilter(bl, al, dat) # ローパスフィルタ適用
    dat_n = signal.lfilter(bn, an, dat) # ノッチフィルタ適用
