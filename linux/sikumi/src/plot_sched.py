import os

import numpy as np
from PIL import Image
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = 'TakaoPGothic'

def plot_sched(concurrency):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for i in range(concurrency):
        x, y = np.loadtxt(f"{i}.data", unpack=True)
        ax.scatter(x, y, s=1)
    ax.set_title(f"scheduler: {concurrency} concurrency")
    ax.set_xlabel("time[ms]")
    ax.set_xlim(0)
    ax.set_ylabel("progress[%]")
    ax.set_ylim([0, 100])
    legend = []
    for i in range(concurrency):
        legend.append(f"loaded process {i}")
    ax.legend(legend)

    pngfilename = f"sched-{concurrency}.png"
    fig.savefig(pngfilename)

def plog_avg_tat(max_nproc):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    x, y, _ = np.loadtext("cpuperf.data", unpack=True)
    ax.scatter(x, y, s=1)
    ax.set_xlim([0, max_nproc+1])
    ax.set_xlabel("process number")
    ax.set_ylim(0)
    ax.set_ylabel("turn around time[ms]")

    pngfilename = "avg-tat.png"
    fig.savefig(pngfilename)

def plot_throughput(max_nproc):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    x, _, y = np.loadtext("cpuperf.data", unpack=True)
    ax.scatter(x, y, s=1)
    ax.set_xlim([0, max_nproc+1])
    ax.set_xlabel("process number")
    ax.set_ylim(0)
    ax.set_ylabel("throughput[process/ms]")

    pngfilename = "throughput.png"
    fig.savefig(pngfilename)
