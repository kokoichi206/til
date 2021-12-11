from utils import argmax
from collections import defaultdict


def eval_onestep(pi, V, env, gamma=0.9):
    delta = 0

    for state in env.states():
        action_probs = pi[state]
        new_v = 0

        for action, action_prob in action_probs.items():
            next_state = env.next_state(state, action)
            if next_state is not None:
                r = env.reward(state, action, next_state)
                new_v += action_prob * (r + gamma * V[next_state])

            delta = max(delta, abs(V[state] - new_v))
            V[state] = new_v
    
    return V, delta

def policy_eval(pi, V, env, gamma, threshold=0.001):
    while True:
        V, delta = eval_onestep(pi, V, env, gamma)
        if delta < threshold:
            break
    return V

def get_greedy_policy(V, env, gamma):
    pi = {}

    for state in env.states():
        action_values = {}

        for action in env.actions():
            next_state = env.next_state(state, action)
            value = 0

            if next_state is not None:
                r = env.reward(state, action, next_state)
                value += r + gamma * V[next_state]
            action_values[action] = value
        
        max_action = argmax(action_values)
        action_probs = {0: 0, 1: 0, 2: 0, 3: 0}
        action_probs[max_action] = 1.0
        pi[state] = action_probs

    return pi

def policy_iter(env, gamma, threshold=0.001, is_render=False):
    pi = defaultdict(lambda: {0: 0.25, 1: 0.25, 2: 0.25, 3: 0.25})
    V = defaultdict(lambda: 0)

    cnt = 0
    while True:
        V = policy_eval(pi, V, env, gamma, threshold)
        new_pi = get_greedy_policy(V, env, gamma)

        if is_render:
            env.render_v(V, pi)
        
        if new_pi == pi:
            break
        pi = new_pi
        
        cnt += 1
        # if cnt % 10 == 0:
        print(pi)

    print(cnt)
    return pi
