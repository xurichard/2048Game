import gym
from gym import spaces
import numpy as np

import Game2048

class Game2048Env(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, size=4):
        self.size = size  # The size of the square grid

        self._game = Game2048.Game2048(size)
        self._game.setupBoard()

        # Observations are dictionaries with the agent's and the target's location.
        # Each location is encoded as an element of {0, ..., `size`}^2, i.e. MultiDiscrete([size, size]).
        self.observation_space = spaces.Dict(
            {
                "board": spaces.Box(0, 131072, shape=(16,), dtype=int), # [(0,0), (0,1), ... ], 2^17 max
                "score": spaces.Discrete(2097152), # (2^17) * 16
            }
        )

        # We have 4 actions, corresponding to "up", "down", "left", "right"
        self.action_space = spaces.Discrete(4)

        """
        The following dictionary maps abstract actions from `self.action_space` to 
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            0: "U",
            1: "D",
            2: "L",
            3: "R",
        }

    def _get_obs(self):
        return {"board": np.array([i for sub in self._game.board for i in sub]), "score": self._game.score}


    def _get_info(self): # add feature vector from the paper?
        return {}

    def reset(self, seed=None, options=None):
        self._game.reset()

        observation = self._get_obs()
        info = self._get_info()

        return observation, info


    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        direction = self._action_to_direction[action]

        changed = self._game.nextState(direction)
        terminated = self._game.lockedBoardState()

        reward = self._game.score

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, False, info

    def render(self):
        self._game.printBoard()



# if __name__ == '__main__':

#     env = Game2048Env()
#     env.render()

#     action = int(input("Enter action:"))
#     state, reward, done, truncated, info = env.step(action)

#     while not done:
#         env.render()
#         action = int(input("Enter action:"))
#         # clear input maybe
#         state, reward, done, truncated, info = env.step(action)












