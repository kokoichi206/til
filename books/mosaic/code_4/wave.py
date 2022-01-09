import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm 


x = np.arange(0, 5, 0.01).reshape(1, -1)
y = np.arange(0, 5, 0.01).reshape(1, -1)
z = np.sin(x + y) # (1000, 1000)



X, Y = np.meshgrid(x, y) 

print(x.shape)
print(y.shape)
print(z.shape)
print(X.shape)
print(Y.shape)

SIZE = 60
fig = plt.figure(figsize=(SIZE,SIZE))
FONTSIZE = 60

Z = (np.sin(X + Y) + 1) / 2
print(Z.shape)
ax = fig.add_subplot(1, 2, 1)
ax.imshow(Z, cmap=cm.gray)
ax.tick_params(axis='x', labelsize=FONTSIZE)
ax.tick_params(axis='y', labelsize=FONTSIZE)

Z = (np.sin(X**2 + Y**2) + 1) / 2
# plt.imshow(Z, cmap=cm.gray) 
# plt.show()
ax = fig.add_subplot(1, 2, 2)
ax.imshow(Z, cmap=cm.gray)
ax.tick_params(axis='x', labelsize=FONTSIZE)
ax.tick_params(axis='y', labelsize=FONTSIZE)

fig.savefig('./wave.png')

