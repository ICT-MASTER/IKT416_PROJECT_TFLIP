import simulation_manager as api
import random
import numpy as np

class Student:

    name = "SBTS Student"

    def __init__(self, id=None, static_epsilon=False, static=False, static_percentage=70):
        # Skill matrix
        self.id = id
        self.matrix = None
        self.history_matrix = None
        self.history_skill = []
        self.hobbit = None
        self.winloss = {
            "win": 0,
            "loss":0
        }

        self.static_epsilon = static_epsilon

        self.decay = 50
        self.epsilon = 0.30


        self.static = static
        self.static_percentage = static_percentage

        self.n_iterations = 0

        self.static_reward = 20
        self.static_punish = 10


    def assign_hobbit(self, hobbit_class):
        self.hobbit = api.assign_hobbit(hobbit_class)
        self.ensure_hobbit()

    def request_taskset(self, num=10):
        self.ensure_hobbit()
        return self.hobbit.generate_taskset(num_tasks=num)


    def get_taskset(self):
        self.ensure_hobbit()
        return self.hobbit.taskset

    def deliver_taskset(self, answer):
        self.hobbit.evaluate_taskset(answer)


    def update_history(self):

        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                self.history_matrix[x][y].append(self.matrix[x][y])

        self.history_skill.append(self.hobbit.get_skill())


    def answer_taskset(self):
        self.ensure_hobbit()

        self.hobbit.cleanup()
        answer = []

        # If using static percentage for rward
        if self.static:
            for task in self.hobbit.taskset:
                cell = self.hobbit.cell_of(task)


                self.n_iterations += 1

                if np.random.random() * 100 < self.static_percentage:
                    self.reward(cell)
                    answer.append((task[0], task[1], True))
                else:
                    self.punish(cell)
                    answer.append((task[0], task[1], False))

                self.update_history()
            return answer



        # Iterate over all tasks in taskset
        for task in self.hobbit.taskset:
            cell = self.hobbit.cell_of(task)
            self.update_history()

            self.n_iterations += 1




            # Retrieve epsilon
            epsilon = self.get_epsilon()


            if np.random.random() < epsilon:
                # Exploit, Use Knowledge about student's previous successes/fails

                # TODO not any good
                p = self.matrix[cell[0]][cell[1]]

                dice = random.random() * 100

                if dice <= p:
                    # Pass
                    answer.append((task[0], task[1], True))
                    self.reward(cell)
                else:
                    # Fail
                    answer.append((task[0], task[1], False))
                    self.punish(cell)

            else:

                # Explore, Random guess which result the student would have produced
                # Guessing its between 30-50% success rate
                if np.random.random() < np.random.uniform(.30, .50):
                    # Pass
                    answer.append((task[0], task[1], True))
                    self.reward(cell)
                else:
                    # Fail
                    answer.append((task[0], task[1], False))
                    self.punish(cell)

        return answer

    def _next_previous(self, cell, multiply, val):
        add_val = multiply * (val / 2)
        next_x = cell[0]
        next_y = cell[1] + (1 * multiply)
        try:
            # Ignore 0 or -1 or bounds on right side of matrix
            if next_y < 0 or next_y >= len(self.matrix[0]):
                return

            self.matrix[next_x][next_y] = max(0, min(100, self.matrix[next_x][next_y] + add_val))
        except:
            pass

    def _lower_upper_or_next_previous(self, cell, multiply, val):
        add_val = multiply * (val / 2)
        next_x = cell[0] + (1 * multiply)
        next_y = cell[1]

        try:
            if next_x <= 0:
                return

            if next_x >= len(self.matrix):
                next_x = 0
                next_y += 1 * multiply

            self.matrix[next_x][next_y] = max(0, min(100, self.matrix[next_x][next_y] + add_val))
        except:
            self._next_previous((0, cell[1]), multiply, val)







    def reward(self, cell):
        # Reward for the cell
        self.matrix[cell[0]][cell[1]] = max(0, min(100, self.matrix[cell[0]][cell[1]] + self.static_reward))

        self._next_previous(cell, 1, self.static_reward)
        self._lower_upper_or_next_previous(cell, 1, self.static_reward)




    def punish(self, cell):
        # Punish for the cell
        self.matrix[cell[0]][cell[1]] = max(0, min(100, self.matrix[cell[0]][cell[1]] - self.static_punish))
        self._next_previous(cell, -1, self.static_punish)
        self._lower_upper_or_next_previous(cell, -1, self.static_punish)


    def get_epsilon(self):
        if self.static_epsilon:
            return self.epsilon

        """Produce epsilon"""
        total = np.sum(self.n_iterations)
        return float(self.decay) / (total + float(self.decay))








    def ensure_hobbit(self):
        if not self.hobbit:
            raise Exception("Hobbit is not initialized for this student!")

