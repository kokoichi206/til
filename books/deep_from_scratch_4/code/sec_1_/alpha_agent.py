import numpy as np

class AlphaAgent:
    def __init__(self, epsilon, alpha, action_size=10):
        self.epsilon = epsilon
        self.qs = np.zeros(action_size)
        self.alpha = alpha

    def update(self, action, reward):
        a, r = action, reward
        self.qs[a] += (r - self.qs[a]) / self.ns[a]

    def get_action(self):
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, len(self.qs))
        return np.argmax(self.qs)

