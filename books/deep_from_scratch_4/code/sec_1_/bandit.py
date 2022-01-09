import numpy as np

class Bandit:
    def __init__(self, arms=10):
        self.arms = arms
        self.rates = np.random.rand(arms)

    def play(self, arm):
        rate = self.rates[arm]
        reward = rate > np.random.rand()
        return int(reward)


if __name__ == "__main__":
    bandit = Bandit(10)
    qs = np.zeros(10)
    ns = np.zeros(10)

    for n in range(10):
        a = np.random.randint(0, 10) # ランダムな行動
        r = bandit.play(a)

        ns[a] += 1
        qs[a] += (r - qs[a]) / ns[a]

