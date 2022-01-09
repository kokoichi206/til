import gym
from dq_agent import DQNAgent
import matplotlib.pyplot as plt

episodes = 300  # 10000
sync_interval = 20
reward_log = []

ave = 5
cnt = 0
for _ in range(ave):
    env = gym.make('CartPole-v0')
    agent = DQNAgent()
    cnt += 1
    print(f"====== {cnt} ======")
    for episode in range(episodes):
        state = env.reset()
        done = False
        sum_reward = 0

        while not done:
            if agent.epsilon > 0.05:
                agent.epsilon -= (1 / 5000)
            # agent.epsilon = max(0.01, 0.1 - 0.09*(episode/200)) #Linear annealing from 10% to 1%
            action = agent.get_action(state)
            next_state, reward, done, info = env.step(action)

            agent.update(state, action, reward, next_state, done)
            state = next_state
            sum_reward += reward

        if episode % sync_interval == 0:
            agent.sync_qnet()

        if cnt == 1:
            reward_log.append(sum_reward)
        else:
            reward_log[episode] += (sum_reward - reward_log[episode]) / cnt
        if episode % 10 == 0:
            print("episode :{}, total reward : {}, epsilon: {}".format(episode, sum_reward, agent.epsilon))


# === Plot ===
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.plot(range(len(reward_log)), reward_log)
# plt.savefig('8.svg')
plt.savefig(f'ave_{ave}.png')
plt.show()


# # === Play CartPole ===
# agent.qnet.save_weights('dqn.npz')
# agent.epsilon = 0  # greedy policy
# state = env.reset()
# done = False
# sum_reward = 0

# while not done:
#     action = agent.get_action(state)
#     next_state, reward, done, info = env.step(action)
#     state = next_state
#     sum_reward += reward
#     env.render()
# print('Total Reward:', sum_reward)
