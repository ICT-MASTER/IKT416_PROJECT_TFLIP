from Algorithms.Hobbit.hobbit_sceptical import hobbit_sceptical as hh_sceptical
from Algorithms.Hobbit.hobbit_ssbt import hobbit_ssbt as hh_ssbt
import simulation_manager as sm
from StudentModel.Student import Student
import matplotlib.pyplot as plt




student = Student(id=1)
student.matrix, student.history_matrix = sm.get_expectation_matrix()
#student.assign_hobbit(hh_ssbt)

student.assign_hobbit(hh_sceptical)




for y in range(100):
    student.request_taskset(num=1)

    answer = []
    for task in student.get_taskset():
        print("----------")
        print("Task is: {0}".format(task))
        inp = input("Did you pass?: ")
        #inp = "y"
        if inp is "y":
            cell = student.hobbit.cell_of(task)
            student.reward(cell)
            answer.append((task[0], task[1], True))
        else:
            cell = student.hobbit.cell_of(task)
            student.punish(cell)
            answer.append((task[0], task[1], False))

    student.deliver_taskset(answer)



    for row_label, row in zip([x.ljust(10, " ") for x in student.hobbit.categories], student.hobbit.matrix):
        print("{0} {1}".format(row_label, ' '.join('%.2f \t' % round(i, 2) for i in row)))


    print("Skill: " + str(student.hobbit.get_skill()))
    print("Sum: " + str(student.hobbit.sum()))

    print("-------------------------------------------------------------------------------------------------")

    for row_label, row in zip([x.ljust(10, " ") for x in student.hobbit.categories], student.matrix):
        print("{0} {1}".format(row_label, ' '.join('%.2f \t' % round(i, 2) for i in row)))

