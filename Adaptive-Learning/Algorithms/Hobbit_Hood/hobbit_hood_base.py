import numpy as np
import random
import os





class hobbit_hood_base:

    def __init__(self, matrix_file = "matrix.csv"):
        self.matrix_file = matrix_file
        self.matrix = None
        self.categories = None

        self._lambda = 0.40 # Learning Rate
        self.beta = 0.4 # Reward/Punish Rate

        self.decay_num_x = 2
        self.decay_num_y = 1

        self._load()


    def _load(self):
        matrix_file_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + self.matrix_file
        # Determine number of columns
        with open(matrix_file_path) as f:
            ncols = len(f.readline().split(','))
            self.categories = [row.split(',')[0] for row in f.readlines()]

        self.matrix = np.loadtxt(matrix_file_path, delimiter=',', skiprows=1, usecols=range(1, ncols))

    def reward(self, cell):
        raise NotImplementedError("reward is not implemented!")

    def punish(self, cell):
        raise NotImplementedError("punish is not implemented!")

    def decay(self, punish_cell):

        # Determine number of cells to reward, punished value
        num_x = self.decay_num_x
        num_y = self.decay_num_y

        # Calculate reward cells
        reward_cells = [(x, punish_cell[1]) for x in range(len(self.matrix)) if x > punish_cell[0] and x <= punish_cell[0] + num_x]
        reward_cells.extend([(punish_cell[0], y) for y in range(len(self.matrix[punish_cell[0]])) if y > punish_cell[1] and y <= punish_cell[1] + num_y])


        # TODO not sure if CORRECT
        if len(reward_cells) is 0:
            reward_cells.append(punish_cell)



        # Calculate new probability for punished cell
        old_probability = self.matrix[punish_cell[0]][punish_cell[1]]
        # new_p = λ * -β * (-p)
        new_probability = old_probability + (self._lambda * self.beta * -old_probability)
        # reward = diff_p / len(reward_cells)
        reward = (old_probability - new_probability) / len(reward_cells)

        # Apply punishment
        self.matrix[punish_cell[0]][punish_cell[1]] = new_probability

        # Apply reward
        for reward_cell in reward_cells:
            self.matrix[reward_cell[0], reward_cell[1]] += reward

    def roulette(self, _decay=False):

        # Create wheel, Format is X,Y,P
        wheel = [{'x': x, 'y': y, 'value': value}for (x,y), value in np.ndenumerate(self.matrix) if value != 0.]

        # Generate random number
        rnd = random.random() * 100
        start = 0
        selected = None
        for item in wheel:
            if rnd > start and rnd < start + item["value"]:
                selected = self.categories[item["x"]], (item["x"], item["y"])
                break
            start += item["value"]

        # Decay if _decay activated
        if _decay:

            self.decay(selected[1])

        return selected

