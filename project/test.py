import gym
import sys
import random
import numpy as np
import os
from collections import deque
from keras.models import Sequential
from keras import Input
from keras.layers import Dense
from keras.optimizers import Adam
import matplotlib.pyplot as plt
from wumpus import Wumpus


# https://towardsdatascience.com/reinforcement-learning-w-keras-openai-dqns-1eed3a5338c
class DQN:
    def __init__(self, env):
        self.history = []
        self.env     = env
        self.memory  = deque(maxlen=10000)
        
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_min = 0.001
        self.epsilon_decay = 0.999
        self.learning_rate = 0.05
        self.tau = 0.125
        self.batch_size = 15

        self.model        = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model   = Sequential()
        state_shape  = self.env.observation_space.__len__()
        model.add(Dense(24, input_dim=state_shape, activation="relu"))
        model.add(Dense(48, activation="relu"))
        model.add(Dense(48, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(self.env.action_space.n))
        model.compile(loss="mean_squared_error", optimizer=Adam(lr=self.learning_rate))
        print(model.summary())
        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        return np.argmax(self.model.predict(state)[0])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        if len(self.memory) < self.batch_size: 
            return

        samples = random.sample(self.memory, self.batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            history = self.model.fit(state, target, epochs=1, verbose=0)
            self.history.append(history.history['loss'][0])

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def graph(self):
        plt.plot(self.history)
        # plt.plot(self.history.history['val_accuracy'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['loss'], loc='upper left')
        plt.show()
        # plt.plot(self.history.history['loss'], label='MAE (testing data)')
        # plt.plot(self.history.history['val_loss'], label='MAE (validation data)')
        # plt.title('MAE for Chennai Reservoir Levels')
        # plt.ylabel('MAE value')
        # plt.xlabel('No. epoch')
        # plt.legend(loc="upper left")
        # plt.show()
        
    def load(self, path):
        if os.path.exists(path):
            self.model.load_weights(path)
            self.target_model.load_weights(path)
        else:
            print("Failed to load weights:", path)

    def save(self, path):
        self.target_model.save_weights(path)


EPISODES = 100
EPISODE_LENGTH = 300
def train():
    env = Wumpus() 
    observation_space = env.observation_space.__len__()
    action_space = env.action_space.n
    dqn_solver = DQN(env)
    dqn_solver.load("model3.h5")
    run = 0
    print("Running", EPISODES, "episodes")
    for _ in range(EPISODES):
        run += 1
        state = env.reset()
        state = np.reshape(state, [1, observation_space])
        score = 0
        step = 0
        action_count = [0] * env.action_space.n
        while True:
            step += 1
            # print("Step:",step)
            # sys.stdout.write("\033[F")
            # env.render()
            action = dqn_solver.act(state)
            action_count[action] += 1
            state_next, reward, terminal, info = env.step(action)
            if step > EPISODE_LENGTH:
               reward -= 2000
            score += reward

            state_next = np.reshape(state_next, [1, observation_space])
            dqn_solver.remember(state, action, reward, state_next, terminal)
            state = state_next

            dqn_solver.replay()
            dqn_solver.target_train()

            if terminal or step > EPISODE_LENGTH:
                print("Run: " + str(run) + ", exploration: " + str(dqn_solver.epsilon) + ", score: " + str(score) + " : " + str(action_count))
                break
        dqn_solver.save('model.h5')
    dqn_solver.graph()


if __name__ == "__main__":
    train()
