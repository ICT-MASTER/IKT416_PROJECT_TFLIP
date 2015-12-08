from .hobbit_hood_base import hobbit_hood_base
import numpy as np
import random
from scipy.stats import norm


class hobbit_hood_ssbt(hobbit_hood_base):

    def __init__(self):
        hobbit_hood_base.__init__(self, matrix_file="matrix_ssbt.csv")

        # Create skill matrix
        self.skill_matrix = np.copy(self.matrix)
        # Set values
        _rows = len(self.skill_matrix)
        for x in range(len(self.skill_matrix)):
            for y in range(len(self.skill_matrix[x])):
                self.skill_matrix[x][y] = ((x) / _rows) + y

        self.student_skill = 0
        self.taskset = None

        self.generate_taskset()



    def generate_taskset(self, num_tasks = 10):

        variance = .5

        relevant_tasks = []
        for x in range(len(self.skill_matrix)):
            for y in range(len(self.skill_matrix[x])):
                item = self.skill_matrix[x][y]
                if self.student_skill >= (item - variance) and self.student_skill <= (item + variance):
                    relevant_tasks.append((x,y))

        # TODO some kinda distribution to select tasks with a percentage of some sort
        taskset = []
        for i in range(num_tasks):
            rnd_task = random.choice(relevant_tasks)
            taskset.append((self.categories[rnd_task[0]], rnd_task[1]))

        self.taskset = taskset
        return self.taskset


    def punish(self, cell):
        x = cell[0]
        y = cell[1]


        skill_points = abs(self.student_skill - self.skill_matrix[x][y]) / self.skill_matrix[x][y]
        print("Student Skill: " + str(self.student_skill))
        print("Task skill: " + str(self.skill_matrix[cell[0]][cell[1]]))
        print("Skill gain: " + str(-skill_points))

        self.student_skill -= skill_points
        self.matrix[x][y] += 1



        pass



    def reward(self, cell):
        x = cell[0]
        y = cell[1]

        skill_points = abs(self.student_skill - self.skill_matrix[x][y]) / self.skill_matrix[x][y]
        print("Student Skill: " + str(self.student_skill))
        print("Task skill: " + str(self.skill_matrix[cell[0]][cell[1]]))
        print("Skill gain: " + str(skill_points))
        self.student_skill += skill_points
        self.matrix[x][y] += 1


        pass












