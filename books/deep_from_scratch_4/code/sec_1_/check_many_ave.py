from bandit import Bandit
from agent import Agent
import numpy as np
import matplotlib.pyplot as plt

epsilons = [0.01, 0.1, 0.3]

fig = plt.figure()
for epsilon in epsilons:
    runs = 2000
    steps = 1000
    # epsilon = 0.1
    all_rates = np.zeros((runs, steps))

    for run in range(runs):
        bandit = Bandit()
        agent = Agent(epsilon)
        sum_r = 0
        rates = []

        for step in range(steps):
            action = agent.get_action()
            reward = bandit.play(action)
            agent.update(action, reward)
            sum_r += reward

            rates.append(sum_r / (step+1))
        
        all_rates[run] = rates

    avg_rates = np.average(all_rates, axis=0)

    plt.ylabel('Rates')
    plt.xlabel('Steps')
    plt.plot(avg_rates, label=epsilon)
plt.legend(bbox_to_anchor=(0.05, 0.95), loc='upper left')
# 下だとうまくいかず（？）
# fig.legend(bbox_to_anchor=(0.05, 0.95), loc='upper left')
fig.savefig('img/rates_many_ave.png')
