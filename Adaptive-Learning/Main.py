__author__ = 'perar'
from Algorithms.Hobbit_Hood.hobbit_hood_sceptical import hobbit_hood_sceptical as hh_sceptical
import simulation_manager as sm
from Student import Student
import matplotlib.pyplot as plt

num_iterations = 1000
num_assignments = 200


# PLOT DATA
history_data = []


# PLOT DATA - END











for x in range(num_iterations):

    student = Student(id=x)
    student.matrix, student.history_matrix = sm.get_expectation_matrix()
    student.assign_hobbit(hh_sceptical)

    for y in range(num_assignments):
        student.request_taskset()
        answer = student.answer_taskset()
        student.deliver_taskset(answer)

    history_data.append(student.history_matrix)


history = history_data[0]
for item in history_data[1:]:
    for x in range(len(item)):
        for y in range(len(item[x])):
            for z in range(len(item[x][y])):
                history[x][y][z] += item[x][y][z]
for x in range(len(history)):
    for y in range(len(history[x])):
        for z in range(len(history[x][y])):
            history[x][y][z] /= len(history_data)


for x in range(len(history)):
    fig, ax = plt.subplots()

    for y_line in range(len(history[x])):
        ax.plot(history[x][y_line], label="{0} - {1}".format(student.hobbit.categories[x], y_line))

    # Now add the legend with some customizations.
    legend = ax.legend(loc='upper right', shadow=True)


    # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    # Set the fontsize
    for label in legend.get_texts():
        label.set_fontsize('large')

    for label in legend.get_lines():
        label.set_linewidth(1.5)  # the legend line width

plt.show()

