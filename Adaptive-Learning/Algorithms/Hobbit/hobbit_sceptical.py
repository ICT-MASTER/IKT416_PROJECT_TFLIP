from .hobbit import hobbit_base
import random
import numpy as np
import math

class hobbit_sceptical(hobbit_base):

    def __init__(self):
        hobbit_base.__init__(self)

        self.taskset = None

        self._lambda = 1  # Learning Rate
        self.beta = None  # Reward / Punish Rate

        self.decay_num_x = 1
        self.decay_num_y = 1

    #  Determine cell of task based on ('while', 0)
    def cell_of(self, task):
        return self.categories.index(task[0]), task[1]

    def generate_taskset(self, num_tasks = 10, do_decay=True):
        if not self.taskset:
            self.taskset = [(task[0], task[1][1]) for task in [self.roulette(_decay=do_decay) for x in range(num_tasks)]]

        return self.taskset

    def punish(self, cell):
        # Determine number of cells to reward, punished value
        num_x = self.decay_num_x
        num_y = self.decay_num_y

        # Calculate punish cells
        reward_cells_x = [(x, cell[1]) for x in range(len(self.matrix)) if x < cell[0] and x >= cell[0] - num_x]
        reward_cells_y = [(cell[0], y) for y in range(len(self.matrix[cell[0]])) if y < cell[1] and y >= cell[1] - num_y]

        reward_cells = reward_cells_x
        reward_cells.extend(reward_cells_y)


    # No reward cells. cannot punish.
        if len(reward_cells) == 0:
            return

        task_skill = (((cell[0] + 1) * (cell[1] + 1)) / len(self.matrix))
        user_skill = self.get_skill()

        #self.beta = task_skill / user_skill
        #self.beta = 1
        x = task_skill - user_skill
        self.beta = 0.50 * math.pow(x, 2) + .5

        # Calculate new probability for punished cell
        old_probability = self.matrix[cell[0]][cell[1]]

        # new_p = λ * -β * (-p)
        new_probability = max(0, old_probability + (self._lambda * self.beta * -old_probability))

        # reward = diff_p / len(reward_cells)
        reward = (old_probability - new_probability) / len(reward_cells)

        # Apply punishment
        self.matrix[cell[0]][cell[1]] = new_probability

        # Apply reward
        for reward_cell in reward_cells:
            self.matrix[reward_cell[0], reward_cell[1]] += reward

    def reward(self, punish_cell):

        # Determine number of cells to reward, punished value
        num_x = self.decay_num_x
        num_y = self.decay_num_y

        # Calculate reward cells
        reward_cells_x = [(x, punish_cell[1]) for x in range(len(self.matrix)) if x > punish_cell[0] and x <= punish_cell[0] + num_x]
        reward_cells_y = [(punish_cell[0], y) for y in range(len(self.matrix[punish_cell[0]])) if y > punish_cell[1] and y <= punish_cell[1] + num_y]

        reward_cells = reward_cells_x
        reward_cells.extend(reward_cells_y)


        # TODO not sure if CORRECT
        if len(reward_cells) is 0:
            reward_cells.append(punish_cell)

        task_skill = (((punish_cell[0] + 1) * (punish_cell[1] + 1)) /  len(self.matrix))
        user_skill = self.get_skill()

        #self.beta = task_skill / user_skill

        x = task_skill - user_skill
        self.beta = 0.50 * math.pow(x, 2) + .5

        #print("User has {0} skill and task is {1} points. Beta: {2}".format(user_skill, task_skill, self.beta))
        # Calculate new probability for punished cell
        old_probability = self.matrix[punish_cell[0]][punish_cell[1]]
        # new_p = λ * -β * (-p)
        new_probability = max(0, old_probability + (self._lambda * self.beta * -old_probability))
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
        #if _decay:
        #    self.punish(selected[1])

        return selected





