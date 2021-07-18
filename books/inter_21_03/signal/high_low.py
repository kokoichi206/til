# import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


def plot_freqz(b, a, title='0.5Hz 1st butterworth HPF'):

    w, h = signal.freqz(b, a, worN=np.logspace(-2, 2, 512),fs=Fs)

    plt.figure()
    plt.subplot(211)
    plt.semilogx(w, 20 * np.log10(np.abs(h)))
    plt.ylim(-45, 5)
    plt.ylabel('Magnitude [dB]')
    plt.title(title)
    plt.grid(which='both', axis='both')
    plt.subplot(212)
    plt.semilogx(w, np.angle(h))
    plt.ylabel('Phase [Rad]')
    plt.xlabel('Frequency [Hz]')
    plt.grid(which='both', axis='both')
    plt.suptitle('Frequency response')
    plt.show()


if __name__ == '__main__':

    Fs = 200
    Fh = 0.5
    Nf = 1
    bh, ah = signal.butter(Nf, Fh, 'high', fs=Fs)

    plot_freqz(bh, ah)
