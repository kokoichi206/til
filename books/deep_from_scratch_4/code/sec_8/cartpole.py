import gym


env = gym.make('CartPole-v0')
state = env.reset()
done = False

while not done:
    env.render()
    action = env.action_space.sample()
    next_state, reward, done, info = env.step(action)
env.close()


# env = gym.make('CartPole-v0')
# state = env.reset()
# print(state)  # 初期状態

# action_space = env.action_space
# print(action_space)  # 行動の次元数

# action = 0  # or 1
# next_state, reward, done, info = env.step(action)
# print(next_state)
# print(next_state, reward, done, info)
