import matplotlib.pyplot as plt
import numpy as np
import os
import random
from collections import deque
from keras.models import Sequential
from keras import Input
from keras.layers import Dense
from keras.optimizers import Adam
from keras.losses import Huber
# https://towardsdatascience.com/reinforcement-learning-w-keras-openai-dqns-1eed3a5338c
class DQNAgent:
    def __init__(self, env, run):
        self.run = run
        self.history = []
        self.env     = env
        self.memory  = deque(maxlen=10000)
        
        self.gamma = 0.95
        if not run:
            self.epsilon = 1.0
            self.epsilon_min = 0.0001
        else:
            self.epsilon = 0.0
            self.epsilon_min = 0.0
        self.epsilon_decay = 0.999
        self.learning_rate = 0.006
        self.tau = 0.8
        self.batch_size = 30

        self.model        = self._create_model()
        self.target_model = self._create_model()
        print(self.model.summary())

    def _create_model(self):
        model   = Sequential()
        state_shape  = self.env.observation_space.__len__()
        model.add(Dense(24, input_dim=state_shape, activation="relu"))
        model.add(Dense(24, activation="relu"))
        model.add(Dense(self.env.action_space.n, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=self.learning_rate))
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
        if len(self.memory) < self.batch_size or self.run: 
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
        self.target_train()
    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def graph(self):
        plt.plot(self.history)
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.show()
        
    def load(self, path):
        if os.path.exists(path):
            self.model.load_weights(path)
            self.target_model.load_weights(path)
        else:
            print("Found no existing weights:", path)

    def save(self, path):
        self.target_model.save_weights(path)

class BayesAgent:
    def __init__(self, env):
        self.env = env
        self.frontier = [] 
        self.explored = []
        self.state = []

    def act(self, state):
        self.state = state
        print(self.state)
        return env.action_space.sample()

    def remember(self, state, action, reward, new_state, done):
        pass

    def replay(self):
        pass

    def _move_to(self, position):
        pass

