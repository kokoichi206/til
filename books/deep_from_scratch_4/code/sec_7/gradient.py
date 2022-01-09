import numpy as np
from dezero import Variable
import matplotlib.pyplot as plt

'''
勾配降下法によって、最小値を求めるプログラム
'''


def rosenbrock(x0, x1):
    y = 100 * (x1 - x0 ** 2) ** 2 + (x0 - 1) ** 2
    return y

# lr = 0.001 # 学習率
iters = 10000 # 繰り返す回数
lrs = [0.001, 0.003, 0.006, 0.0005] # 学習率
lr = 0.006
fig = plt.figure()

for lr in lrs:
    x0_array = []
    x1_array = []
    x0 = Variable(np.array(0.0))
    x1 = Variable(np.array(2.0))
    for i in range(iters):
        # print(x0, x1)
        x0_array.append(x0.data.tolist())
        x1_array.append(x1.data.tolist())
        y = rosenbrock(x0, x1)

        x0.cleargrad()
        x1.cleargrad()
        y.backward()

        x0.data -= lr * x0.grad.data
        x1.data -= lr * x1.grad.data

    plt.scatter(x0_array, x1_array, label=lr)
plt.legend(bbox_to_anchor=(0.95, 0.95), loc='upper right', title='lr')
fig.savefig('./gradient_descent_method.png')
