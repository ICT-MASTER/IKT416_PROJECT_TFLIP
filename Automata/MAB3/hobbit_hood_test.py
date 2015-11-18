import numpy
import random
import numpy as np





loll = None

def load_tag_matrix():
    # List of all the tags (IE: while, for)
    tags = []

    # Matrix with all probabilities
    tags_matrix = None

    # Open the tags matrix
    with open("data.csv", "r") as file:

        # Read all lines
        lines = file.readlines()

        # Determine number of columns in matrix
        matrix_columns = len(lines[0].split(";")) - 1

        # Determine number of rows in matrix
        matrix_rows = len(lines) - 1

        # Define matrix
        tags_matrix = numpy.zeros((matrix_rows, matrix_columns))

        # Populate matrix
        x = 0
        for row in lines[1:]:
            columns = row.split(";")

            tags.append(columns[0])

            y = 0
            for column in columns[1:]:
                tags_matrix[x][y] = column

                y += 1
            x += 1
    return tags, tags_matrix


def roulette(tags_matrix, decay=None):
    # If decay is set
    if decay:

        ########################################
        #
        #
        #
        ########################################
        _lambda = 1.0
        beta = 0.4

        ########################################
        #
        # Current probability
        #
        ########################################
        probability = tags_matrix[decay[0]][decay[1]]

        ########################################
        #
        # Determine cells to reward
        # The logic behind this is to:
        # * reward all cells below decay in same column
        # * reward cell in same row, next column
        #
        ########################################
        # Cells in same column below decay's row
        reward_cells = [(x, 0) for x in range(len(tags_matrix)) if x > decay[0]]
        # Cell in same row, next column
        reward_cells.append((decay[0], min(len(tags_matrix[0]) - 1, decay[1] + 1)))

        ########################################
        #
        # Calculate punish and reward value
        # * punish = λ * -β * (1 - probability)
        # * reward = |punish| / len(reward_cells)
        #
        ########################################
        punish = np.multiply( np.multiply(_lambda, beta * (-1)), (100 - probability))
        reward = np.divide(np.abs(punish), len(reward_cells))

        # Calculate next_probability for decay
        next_probability = tags_matrix[decay[0]][decay[1]] + punish

        ########################################
        #
        # Mechanism which handles cases where next_probability is <= 0
        # What it does is to remove the value which is below zero and subtract it from rest of the reward cells.
        #
        ########################################
        if next_probability <= 0:
            delta_add = np.divide(abs(next_probability), len(reward_cells))
            tags_matrix[decay[0]][decay[1]] = 0.0000000
            reward = np.subtract(reward, delta_add)
        else:
            tags_matrix[decay[0]][decay[1]] = next_probability

        ########################################
        #
        # Reward all "reward_cells"
        #
        ########################################
        for reward_cell in reward_cells:
            tags_matrix[reward_cell[0], reward_cell[1]] += reward



    ########################################
    #
    # wheel_tag_indexes:
    # wheel: the wheel itself,
    ########################################
    wheel_tag_indexes = []
    wheel = []

    # Start of the wheel
    start = .0

    # Determine row and column length of the matrix
    rows = len(tags_matrix)
    cols = len(tags_matrix[0])

    # Set current to start (0)
    current = start

    # loop through the matrix, but start with rows (Want it ordered by level)
    for y in range(cols):
        for x in range(rows):

            # Retrieve an item from matrix
            item = tags_matrix[x][y]

            # Calculate next current value
            next_current = current + item

            # Ignore if no difference or negative
            if current == next_current or current > next_current:
                continue

            # Add range
            wheel_tag_indexes.append([tags[x], y])
            wheel.append([np.around(current, 5), np.around(next_current, 5), (x, y)])

            # Set new current
            current = next_current

    ########################################
    #
    # Wheel is created, use the wheel by running a dice from 0 to 100
    # Check each of the wheel array values and validate if its between current item (For loop)
    #
    ########################################
    # Create random between 0 to 100
    rnd = random.random() * 100

    # Iterate over the wheel
    for i in range(len(wheel)):

        # Fetch the wheel range for current iteration
        p_range = wheel[i]

        # Check if random value is between the random number
        # Return wheel item if true
        if rnd > p_range[0] and rnd < p_range[1]:
            return wheel_tag_indexes[i], wheel[i][2]







# Load the tag_matrix
tags, tags_matrix = load_tag_matrix()



########################################
#
# Run algorithm
# num_tasks: Number of tasks to generate for the student set
# decay: decay is set in order to decay the probability of an already selected task
# this is done so the chance of getting the same category + level twice is decreeased
########################################
# Num tasks to generate
num_tasks = 10

tasks = []
decay = None
for i in range(num_tasks):


    # Roulette for a task
    task = roulette(tags_matrix, decay)

    # Set decay index for next iteration
    decay = task[1]

    # Add task to list of tasks
    tasks.append((tags[task[1][0]], task[1][1]))



print(tasks)
print("Matrix sum: " + str(np.sum(tags_matrix)))

