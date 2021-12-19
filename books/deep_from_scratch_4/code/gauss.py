import numpy as np
import matplotlib.pyplot as plt

samples = 1000
action_size = 4
Q_list = []

# max を取ることで、過大評価されている
for _ in range(samples):
    Q = np.random.randn(action_size)
    Q_list.append(Q.max())

plt.hist(Q_list, bins=16)
plt.axvline(x=0, color="red")
plt.show()




# ======================================
# Double DQN
# ======================================
samples = 1000
action_size = 4
Q_list = []

for _ in range(samples):
    Q = np.random.randn(action_size)
    Q_prime = np.random.randn(action_size)  # 別のQ関数
    idx = np.argmax(Q) 
    Q_list.append(Q_prime[idx])

plt.hist(Q_list, bins=16)
plt.axvline(x=0, color="red")
plt.show()