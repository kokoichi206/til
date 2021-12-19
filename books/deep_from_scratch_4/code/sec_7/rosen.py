from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from dezero import Variable




def rosenbrock(x0, x1):
    y = 100 * (x1 - x0 ** 2) ** 2 + (x0 - 1) ** 2
    return y

lr = 0.001
x0_array = []
x1_array = []
x0 = Variable(np.array(0.0))
x1 = Variable(np.array(2.0))
for i in range(100):
    # print(x0, x1)
    x0_array.append(x0.data.tolist())
    x1_array.append(x1.data.tolist())
    y = rosenbrock(x0, x1)

    x0.cleargrad()
    x1.cleargrad()
    y.backward()

    x0.data -= lr * x0.grad.data
    x1.data -= lr * x1.grad.data

#     plt.scatter(x0_array, x1_array, label=lr)
# plt.legend(bbox_to_anchor=(0.95, 0.95), loc='upper right', title='lr')
# fig.savefig('./gradient_descent_method.png')




def func1(x, y):
    return 100 * (x - y**2)**2 + (y - 1)**2 

x = np.arange(0.0, 2.0, 0.1)
y = np.arange(0.0, 1.1, 0.1)

X, Y = np.meshgrid(x, y)
Z = func1(X, Y)

fig = plt.figure()
ax = Axes3D(fig)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("f(x, y)")

ax.scatter([1.0], [1.0], c="red")
ax.scatter(x1_array, x0_array, c="green")

ax.plot_wireframe(X, Y, Z)
plt.show()
