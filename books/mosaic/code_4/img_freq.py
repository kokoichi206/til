import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm 


x = np.arange(0, 5, 0.01).reshape(1, -1)
y = np.arange(0, 5, 0.01).reshape(1, -1)
z = np.sin(x + y) # (1000, 1000)

X, Y = np.meshgrid(x, y) 

SIZE = 40
FONTSIZE = 60
fig = plt.figure(figsize=(SIZE,SIZE))

a = [0.1, 1, 10]
b = [0.1, 1, 10]
len_a = len(a)
len_b = len(b)
for i in range(len_a):
    for j in range(len_b):
        Z = (np.sin(a[i]*X + b[j]*Y) + 1) / 2
        ax = fig.add_subplot(len_a, len_b, len_b*i+j+1)
        ax.imshow(Z, cmap=cm.gray)
        ax.axis('off')
        ax.set_title(f"a={a[i]},b={b[j]}", fontsize=FONTSIZE)
fig.savefig('./img_freq.png')
