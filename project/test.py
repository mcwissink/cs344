import gym
import random
import numpy as np
import os
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from wumpus import Wumpus

GAMMA = 0.95
LEARNING_RATE = 0.001

MEMORY_SIZE = 1000000
BATCH_SIZE = 500

EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.01
EXPLORATION_DECAY = 0.995


class DQNSolver:

    def __init__(self, observation_space, action_space):
        self.exploration_rate = EXPLORATION_MAX

        self.action_space = action_space
        self.memory = deque(maxlen=MEMORY_SIZE)

        self.model = Sequential()
        self.model.add(Dense(24, input_shape=(observation_space,), activation="relu"))
        self.model.add(Dense(24, activation="relu"))
        self.model.add(Dense(self.action_space, activation="linear"))
        self.model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() < self.exploration_rate:
            return random.randrange(self.action_space)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def experience_replay(self):
        if len(self.memory) < BATCH_SIZE:
            return
        batch = random.sample(self.memory, BATCH_SIZE)
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            if not terminal:
                q_update = (reward + GAMMA * np.amax(self.model.predict(state_next)[0]))
                q_values = self.model.predict(state)
                q_values[0][action] = q_update
                self.model.fit(state, q_values, verbose=0)
                self.exploration_rate *= EXPLORATION_DECAY
                self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)

    def load(self, path):
        if os.path.exists(path):
            self.model.load_weights(path)
        else:
            print("Failed to load weights:", path)

    def save(self, path):
        self.model.save_weights(path)


EPISODES = 3000
def train():
    env = Wumpus() 
    observation_space = env.observation_space.__len__()
    action_space = env.action_space.n
    dqn_solver = DQNSolver(observation_space, action_space)
    dqn_solver.load("my_model.h5")
    run = 0
    print("Running", EPISODES, "episodes")
    for _ in range(EPISODES):
        run += 1
        state = env.reset()
        state = np.reshape(state, [1, observation_space])
        step = 0
        while True:
            step += 1
            # env.render()
            action = dqn_solver.act(state)
            state_next, reward, terminal, info = env.step(action)
            state_next = np.reshape(state_next, [1, observation_space])
            dqn_solver.remember(state, action, reward, state_next, terminal)
            state = state_next
            if terminal:
                print("Player, gold:", env.player["gold"])
                print("Run: " + str(run) + ", exploration: " + str(dqn_solver.exploration_rate) + ", actions: " + str(step))
                break
            dqn_solver.experience_replay()
    dqn_solver.save('my_model.h5')


if __name__ == "__main__":
    train()
