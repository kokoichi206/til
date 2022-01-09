import bandit
import agent
import matplotlib.pyplot as plt

if __name__ == "__main__":
    steps = 1000
    epsilon = 0.1

    bandit = bandit.Bandit()
    agent = agent.Agent(epsilon)
    sum_r = 0
    total_rewards =  []
    rates = []

    for step in range(steps):
        action = agent.get_action()
        reward = bandit.play(action)
        agent.update(action, reward)
        sum_r += reward

        total_rewards.append(sum_r)
        rates.append(sum_r / (step+1))
    
    print(sum_r)

    fig = plt.figure()

    plt.ylabel('Total reward')
    plt.xlabel('Steps')
    plt.plot(total_rewards)
    # plt.show()
    fig.savefig('img/total_rewardsv.png')
    plt.clf()

    plt.ylabel('Rates')
    plt.xlabel('Steps')
    plt.plot(rates)
    # plt.show()
    fig.savefig('img/rates.png')
