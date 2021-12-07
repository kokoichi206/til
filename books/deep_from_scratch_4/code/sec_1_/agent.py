import numpy as np

class Agent:
    def __init__(self, epsilon, action_size=10):
        self.epsilon = epsilon
        self.qs = np.zeros(action_size)
        self.ns = np.zeros(action_size)

    def update(self, action, reward):
        a, r = action, reward
        self.ns[a] += 1
        self.qs[a] += (r - self.qs[a]) / self.ns[a]

    def get_action(self):
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, len(self.qs))
        return np.argmax(self.qs)
