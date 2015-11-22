from hobbit_hood_base import hobbit_hood_base


class hobbit_hood_sceptical(hobbit_hood_base):

    def __init__(self):
        hobbit_hood_base.__init__(self)

        self.taskset = None
        self.generate_taskset()


    def generate_taskset(self, num_tasks = 10, do_decay = True):
        if not self.taskset:
            self.taskset = [(task[0], task[1][1]) for task in [self.roulette(_decay = do_decay) for x in range(num_tasks)]]

        return self.taskset

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


    def punish(self, cell):
        # Determine number of cells to reward, punished value
        num_x =  self.decay_num_x
        num_y = self.decay_num_y

        # Calculate reward cells
        reward_cells = [(x, cell[1]) for x in range(len(self.matrix)) if x < cell[0] and x >= cell[0] - num_x]
        reward_cells.extend([(cell[0], y) for y in range(len(self.matrix[cell[0]])) if y < cell[1] and y >= cell[1] - num_y])

        # No reward cells. cannot punish.
        if len(reward_cells) == 0:
            return

        # Calculate new probability for punished cell
        old_probability = self.matrix[cell[0]][cell[1]]
        # new_p = λ * -β * (-p)
        new_probability = old_probability + (self._lambda * self.beta * -old_probability)
        # reward = diff_p / len(reward_cells)
        reward = (old_probability - new_probability) / len(reward_cells)

        # Apply punishment
        self.matrix[cell[0]][cell[1]] = new_probability

        # Apply reward
        for reward_cell in reward_cells:
            self.matrix[reward_cell[0], reward_cell[1]] += reward



    def reward(self, cell):
        self.decay(cell)











