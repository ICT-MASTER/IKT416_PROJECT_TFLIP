from Algorithms.Hobbit_Hood.hobbit_hood_sceptical import hobbit_hood_sceptical as hh_sceptical
import simulation_manager as sm
from Student import Student
import matplotlib.pyplot as plt




student = Student(id=1)
student.matrix, student.history_matrix = sm.get_expectation_matrix()
student.assign_hobbit()


for y in range(200):
    student.request_taskset(num=1)

    for task in student.get_taskset():
        print("----------")
        print("Task is: {0}".format(task))
        #inp = input("Did you pass?: ")
        inp = "y"
        if inp is "y":
            student.deliver_taskset([(task[0], task[1], True)])
        else:
            student.deliver_taskset([(task[0], task[1], False)])



for row_label, row in zip([x.ljust(10, " ") for x in student.hobbit.categories], student.hobbit.matrix):
    print("{0} {1}".format(row_label, ' '.join('%.2f \t' % round(i, 2) for i in row)))

print("Skill: " + str(student.hobbit.get_skill()))
