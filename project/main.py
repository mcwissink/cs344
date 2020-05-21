import numpy as np
import matplotlib.pyplot as plt
from wumpus import Wumpus
from agent import DQNAgent
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", help="The name of the model to load/save", default="model")
parser.add_argument("-r", "--run", help="Run a trained model", action="store_true")
parser.add_argument("-e", "--episodes", type=int, help="Number of episodes to run/train", default=100)
parser.add_argument("--maxsteps", type=int, help="The max steps in an episode. Prevents bot from looping", default=1000)
args = parser.parse_args()

weights_file = re.sub(r"\.h5$", "", args.filename) + ".h5"

def train():
    env = Wumpus() 
    observation_space = env.observation_space.__len__()
    action_space = env.action_space.n
    agent = DQNAgent(env, run=args.run)
    scores = []
    agent.load(weights_file)
    print("Running", args.episodes, "episodes")
    run = 0
    for _ in range(args.episodes):
        run += 1
        state = env.reset()
        state = np.reshape(state, [1, observation_space])
        score = 0
        step = 0
        action_count = [0] * env.action_space.n
        while True:
            step += 1
            # print("Step:",step)
            env.render()
            action = agent.act(state)
            action_count[action] += 1
            state_next, reward, terminal, info = env.step(action)
            score += reward

            state_next = np.reshape(state_next, [1, observation_space])
            agent.remember(state, action, reward, state_next, terminal)
            state = state_next

            agent.replay()

            if terminal or step > args.maxsteps:
                print("Run: " + str(run) + ", exploration: " + str(agent.epsilon) + ", score: " + str(score) + " : " + str(action_count))
                scores.append(score)
                break
        agent.save(weights_file)
    agent.graph()
    plt.plot(scores)
    plt.title('score')
    plt.ylabel('score')
    plt.xlabel('episode')
    plt.show()

if __name__ == "__main__":
    train()
