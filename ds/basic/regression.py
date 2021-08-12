from __future__ import print_function, division

import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


N = 500
X = np.random.random((N, 2))*4 - 2 # in between (-2, 2)
Y = X[:,0]*X[:,1]   # makes a saddle shape

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,0], X[:,1], Y)
plt.show()


D = 2
M = 100

# layer 1
W = np.random.randn(D, M) / np.sqrt(D)
b = np.zeros(M)

# layer 2
V = np.random.randn(M) / np.sqrt(M)
c = 0


# how to get the output
def forward(X):
    Z = X.dot(W) + b
    Z = Z * (Z > 0) # relu
    # Z = np.tanh(Z)

    Yhat = Z.dot(V) + c
    return Z, Yhat


# how to train the params
def derivative_V(Z, Y, Yhat):
    return (Y - Yhat).dot(Z)

def derivative_c(Y, Yhat):
    return (Y - Yhat).sum()

def derivative_W(X, Z, Y, Yhat, V):
    dZ = np.outer(Y - Yhat, V) * (Z > 0) # relu
    return X.T.dot(dZ)

def derivative_b(Z, Y, Yhat, V):
    dZ = np.outer(Y - Yhat, V) * (Z > 0) # this is for relu activation
    return dZ.sum(axis=0)

def update(X, Z, Y, Yhat, W, b, V, c, learning_rate=1e-4):
    gV = derivative_V(Z, Y, Yhat)
    gc = derivative_c(Y, Yhat)
    gW = derivative_W(X, Z, Y, Yhat, V)
    gb = derivative_b(Z, Y, Yhat, V)

    V += learning_rate*gV
    c += learning_rate*gc
    W += learning_rate*gW
    b += learning_rate*gb

    return W, b, V, c


# so we can plot the costs later
def get_cost(Y, Yhat):
    return ((Y - Yhat)**2).mean()


# run a training loop
# plot the cost
costs = []
for i in range(200):
    Z, Yhat = forward(X)
    W, b, V, c = update(X, Z, Y, Yhat, W, b, V, c)
    cost = get_cost(Y, Yhat)
    costs.append(cost)
    if i % 25 == 0:
        print(cost)

# plot the costs
plt.plot(costs)
plt.show()


# plot the prediction with the data
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,0], X[:,1], Y)

# surface plot
line = np.linspace(-2, 2, 20)
xx, yy = np.meshgrid(line, line)
Xgrid = np.vstack((xx.flatten(), yy.flatten())).T
_, Yhat = forward(Xgrid)
ax.plot_trisurf(Xgrid[:,0], Xgrid[:,1], Yhat, linewidth=0.2, antialiased=True)
plt.show()

