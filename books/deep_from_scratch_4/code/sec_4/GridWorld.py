import numpy as np

from eval import policy_iter


class GridWorld:
    def __init__(self):
        self.action_space = [0, 1, 2, 3]
        self.action_meaning = {
            0: "UP",
            1: "DOWN",
            2: "LEFT",
            3: "RIGHT",
        }
        self.reward_map = np.array(
            [
                [0, 0, 0, 1.0],
                [0, None, 0, -1.0],
                [0, 0, 0, 1.0],
            ]
        )
        self.goal_state = (0, 3)
        self.start_state = (2, 0)
        self.agent_state = self.start_state

    @property
    def height(self):
        return len(self.reward_map)

    @property
    def width(self):
        return len(self.reward_map[0])

    @property
    def shape(self):
        return self.reward_map.shape

    def actions(self):
        return self.action_space    # [0, 1, 2, 3]
    
    def states(self):
        for h in range(self.height):
            for w in range(self.width):
                yield (h, w)
    
    def next_state(self, state, action):
        is_goal = (state == self.goal_state)
        is_wall = (self.reward_map[state] is None)
        if is_goal or is_wall:
            return None
        
        action_move_map = [(-1, 0), (1,0), (0, -1), (0, 1)]
        move = action_move_map[action]
        next_state = (state[0] + move[0], state[1] + move[1])
        ny, nx = next_state

        if nx < 0 or nx >= self.width or ny < 0 or ny >=self.height or \
                self.reward_map[next_state] is None:
            next_state = state
        
        return next_state

    # r(s,a,s') の引数に対応させている
    def reward(self, state, action, next_state):
        return self.reward_map[next_state]

    def reset(self):
        self.agent_state = self.start_state
        return self.agent_state

    def step(self, action):
        state = self.agent_state
        next_state = self.next_state(state, action)
        reward = self.reward(state, action, next_state)
        done = (next_state == self.goal_state)

        self.agent_state = next_state
        return next_state, reward, done


if __name__ == '__main__':
    env = GridWorld()
    gamma = 0.9
    pi = policy_iter(env, gamma)
