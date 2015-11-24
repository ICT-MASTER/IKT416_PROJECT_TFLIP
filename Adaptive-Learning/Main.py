__author__ = 'perar'
from Algorithms.Hobbit_Hood.hobbit_hood_sceptical import hobbit_hood_sceptical as hh_sceptical
import simulation_manager as sm
from Student import Student
import matplotlib.pyplot as plt


num_students = 1





for x in range(num_students):

    student = Student(id=x)
    student.matrix, student.history_matrix = sm.get_expectation_matrix()
    student.assign_hobbit()


    for y in range(200):
        student.request_taskset()
        answer = student.answer_taskset()
        student.deliver_taskset(answer)



    for x in range(len(student.history_matrix)):
        fig, ax = plt.subplots()

        for y_line in range(len(student.history_matrix[x])):
                ax.plot(student.history_matrix[x][y_line], label="{0} - {1}".format(student.hobbit.categories[x], y_line))

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




    print(student.matrix)
    print(student.hobbit.matrix)
















