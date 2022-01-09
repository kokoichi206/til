import numpy as np
from dezero import Variable
import dezero.functions as F

x_np = np.array(2.0)
x = Variable(x_np)

y = 3 * x ** 2
print(y)

y.backward()
print(x.grad)


a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
a, b = Variable(a), Variable(b) # 省略可
c = F.matmul(a, b)
print(c)

a = np.array([[1, 2], [3, 4]])
b = np.array([[1, 2], [3, 4]])
c = F.matmul(a, b)
print(c)


