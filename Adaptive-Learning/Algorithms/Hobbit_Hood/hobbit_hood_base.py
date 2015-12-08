import numpy as np
import random
import os





class hobbit_hood_base:

    def __init__(self, matrix_file = "matrix.csv"):
        self.matrix_file = matrix_file
        self.matrix = None
        self.categories = None


        self._load()

    def _load(self):
        matrix_file_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + self.matrix_file
        # Determine number of columns
        with open(matrix_file_path) as f:
            n_cols = len(f.readline().split(','))
            self.categories = [row.split(',')[0] for row in f.readlines()]


        self.matrix = np.loadtxt(matrix_file_path, delimiter=',', skiprows=1, usecols=range(1, n_cols))

    def reward(self, cell):
        raise NotImplementedError("reward is not implemented!")

    def punish(self, cell):
        raise NotImplementedError("punish is not implemented!")

    def evaluate_taskset(self, taskset_ans):

        for task in taskset_ans:
            task_type = task[0]
            task_level = task[1]
            try:
                task_passed = task[2]
            except:
                task_passed = False

            cell = (self.categories.index(task_type), task_level)

            # If task was passed, punish task's position in matrix
            if task_passed:
                self.reward(cell)
            # If task was NOT passed, reward task's position in matrix
            else:
                self.punish(cell)

        self.taskset = None


    def get_skill(self):

        num_categories = len(self.matrix)
        count = 0
        skill = 0

        for y in range(len(self.matrix[0])):
            for x in range(len(self.matrix)):
                count += 1
                cell = self.matrix[x][y]
                cell_difficulty = (count / num_categories)
                skill += ((cell/100) * cell_difficulty)

        return skill


    # Determine cell of task based on ('while', 0)
    def cell_of(self, task):
        return self.categories.index(task[0]), task[1]

