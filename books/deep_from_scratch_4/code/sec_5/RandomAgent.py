from collections import defaultdict
import numpy as np


class RandomAgent:
    def __init__(self):
        self.gamma = 0.9
        self.action_size = 4

        random_actions = {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25}
        self.pi = defaultdict(lambda: random_actions)
        self.V = defaultdict(lambda: 0)
        self.cnts = defaultdict(lambda: 0)
        self.experience = []
    
    def get_action(self, state):
        ps = self.pi[state]
        actions, probs = list(ps.keys()), list(ps.values())
        return np.random.choice(actions, p=probs)

    def add(self, state, action, next_reward):
        data = (state, action, next_reward)
        self.experience.append(data)

    def reset(self):
        self.experience = []
    
    def eval(self):
        g = 0
        for data in reversed(self.experience):
            state, action, next_reward = data
            g = self.gamma * g + next_reward
            self.cnts[state] += 1
            self.V[state] += (g - self.V[state]) / self.cnts[state]

