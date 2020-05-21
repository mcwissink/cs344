import sys
import gym
from gym import spaces
import numpy as np
import random
from enum import IntEnum
import math

class Wumpus(gym.Env):
    metadata = {'render.modes': ['human']}   
    class Board(IntEnum):
        NOTHING = 0
        PIT = 1
        BREEZE = 2
        WUMPUS = 3
        STENCH = 4
        GOLD = 5
        PLAYER = 6
        EXIT = 7
        WALL = 8

    class Direction(IntEnum):
        UP = 0
        LEFT = 1
        DOWN = 2
        RIGHT = 3

    class Actions(IntEnum):
        FORWARD = 0
        TURNLEFT = 1
        TURNRIGHT = 2
        GRAB = 3
        SHOOT = 4
        CLIMB = 5

    class Rewards(IntEnum):
        EXIT = -500
        EXIT_GOLD = 1000
        DEATH = -1000
        GRAB_GOLD = 500
        
    def __init__(self, width=4, height=4):
        self.w = width
        self.h = height
        self.player = {
            "position": 0,
            "direction": 0, 
            "arrow": True,
            "gold": False,
        }
        self.action = 0
        self.reward = 0
        self.observations = []
        self.action_space = spaces.Discrete(6)

        self.observation_space = spaces.Tuple((
            spaces.Discrete(2),
            spaces.Discrete(2),
            spaces.Discrete(2),
            spaces.Discrete(2),
            spaces.Discrete(2),
            spaces.Discrete(2),
            spaces.Discrete(self.w * self.h),
            spaces.Discrete(4),
            spaces.Discrete(2),
        ))
        self._generate()
    
    def step(self, action):
        assert self.action_space.contains(action)
        observations = [False] * 9
        done = False
        reward = -1
        # Handle the actions
        if action == self.Actions.FORWARD:
            position, bump = self._move_forward(self.player["position"], self.player["direction"], self.Board.PLAYER)
            observations[3] = bump
            # if not bump:
            #     reward += 1
            self.player["position"] = position
        elif action == self.Actions.TURNLEFT:
            self.player["direction"] = self._turn_left(self.player["direction"])
        elif action == self.Actions.TURNRIGHT:
            self.player["direction"] = self._turn_right(self.player["direction"])
        elif action == self.Actions.GRAB:
            if self.Board.GOLD in self.board[self.player["position"]]:
                print("GOT GOLD!")
                reward += self.Rewards.GRAB_GOLD
                self.player["gold"] = True
                self.board[self.player["position"]].remove(self.Board.GOLD)
        elif action == self.Actions.SHOOT:
            reward -= 20
            pass
        elif action == self.Actions.CLIMB:
            if self.Board.EXIT in self.board[self.player["position"]]:
                print("EXITED!")
                reward += self.Rewards.EXIT_GOLD if self.player["gold"] else self.Rewards.EXIT
                done = True

        # Check if the player died
        position = self.board[self.player["position"]]
        if self.Board.PIT in position or self.Board.WUMPUS in position:
            print("DIED!")
            reward -= 1000
            done = True
        observations = self._get_observations(observations)

        # Record things for rendering
        self.action = action
        self.reward = reward
        self.observations = observations
        
        return np.array(observations), reward, done, {}
            
    def reset(self):
        self.player = {
            "position": 0,
            "direction": 0, # 0 = up, 1 = left, 2 = down, 3 = right
            "arrow": True,
            "gold": False,
        }
        self._generate();
        return self._get_observations()

    
    def render(self, mode='human', close=False):
        out = sys.stdout
        for i in range(self.h):
            for j in range(self.w):
                #out.write("" + np.sum(list(self.board[i * self.h + j])).tostring())
                out.write("{} ".format(np.sum(list(self.board[i * self.h + j]))))
            out.write("\n")
        out.write("Action: {}, Reward: {}\n".format(self.action, self.reward))
        print(self.observations)
        for i in range(self.h + 2):
            sys.stdout.write("\033[F")

    def _get_observations(self, observations=[False] * 9):
        position = self.board[self.player["position"]]
        observations[0] = self.Board.STENCH in position
        observations[1] = self.Board.BREEZE in position
        observations[2] = self.Board.GOLD in position
        observations[5] = self.Board.EXIT in position
        observations[6] = self.player["position"]
        observations[7] = self.player["direction"]
        observations[8] = self.player["gold"]
        
        return observations

    def _move_forward(self, position, direction, item=None):
        new_position = position
        distance = self.h if direction % 2 == 0 else 1
        sign = -1 if direction < 2 else 1
        move_to = position + (distance * sign)
        new_position = move_to if self._valid_move(position, move_to) and self.Board.WALL not in self.board[move_to] else position
        if item is not None:
            self.board[position].discard(item)
            self.board[new_position].add(item)
        return new_position, position == new_position

    def _valid_move(self, old, new):
        old_row = math.floor(old/self.w)
        new_row = math.floor(new/self.w)
        diff = abs(old - new)
        if diff == 1:
            return old_row == new_row
        elif diff == self.w:
            return new_row >= 0 and new_row < self.h
        else:
            return False

    def _turn_left(self, direction):
        return (direction + 1) % 4

    def _turn_right(self, direction):
        return (direction - 1) % 4

    def _is_empty(self, position):
        p = self.board[position]
        return not (self.Board.PIT in p or self.Board.EXIT in p or self.Board.WALL in p or self.Board.PLAYER in p or self.Board.WUMPUS in p or self.Board.GOLD in p)

    def _random_empty_place(self, item=None):
        rand = random.randrange(len(self.board))
        for i in range(len(self.board)):
            p = (rand + i) % len(self.board)
            if self._is_empty(p):
                if item is not None:
                    self.board[p].add(item)
                return p 
        print("Failed to place item")
        return -1
                
    def _get_adjacent(self, position):
        adj = []
        for direction in range(4):
            distance = self.h if direction % 2 == 0 else 1
            sign = -1 if direction < 2 else 1
            move_to = position + (distance * sign)
            if self._valid_move(position, move_to):
                adj.append(move_to)
        return adj
            

    def _generate(self):
        self.board = [{0} for _ in range(self.h * self.w)]

        start_position = 12
        self.board[start_position].add(self.Board.PLAYER)
        self.board[start_position].add(self.Board.EXIT)
        self.player["position"] = start_position

        for i in range(len(self.board)):
            if random.uniform(0, 1) < 0.1:
                if (self._is_empty(i)):
                    self.board[i].add(self.Board.PIT)
                    for j in range(4):
                        self._move_forward(i, j, self.Board.BREEZE)
                    
        # Place the gold at a random spot
        self._random_empty_place(self.Board.GOLD)

if __name__ == "__main__":
    board = Wumpus()
    print(board._get_adjacent(0))
    print(board._get_adjacent(1))
    print(board._get_adjacent(5))

