
import simulation_manager as sm
from StudentModel.Student import Student
from Algorithms.Hobbit.hobbit_sceptical import hobbit_sceptical as hh_sceptical
import multiprocessing
import matplotlib.pyplot as plt
from xvfbwrapper import Xvfb

vdisplay = Xvfb()
vdisplay.start()


def worker(
        x,
        model,
        num_students=10,
        num_assignments=1
):
    #print("{0} of {1} | ({2}%)".format(x, num_students, (x/num_students)*100.0))

    # Initialize a student
    student = model(id=x)
    student.static = True
    student.static_percentage = x

    #  Init expectation matrix
    student.matrix, student.history_matrix = sm.get_expectation_matrix()
    student.assign_hobbit(hh_sceptical)

    # Request taskset for student
    for y in range(num_assignments):
        student.request_taskset(num=num_assignments)
        answer = student.answer_taskset()
        student.deliver_taskset(answer)

    # Return student
    return student



def run(num_students, num_assignments, times):

    skill_data_per_percentage = [0 for x in range(100)]
    skill_data_per_percentage_epsilon_greedy = [0 for x in range(100)]

    pool = multiprocessing.Pool(processes=20)

    n = times
    for i in range(n):
        print("{0}/{1}".format(i,n))
        results = [pool.apply_async(worker, args=(x, Student, num_students, num_assignments)) for x in range(num_students)]
        output = [p.get() for p in results]

        for student in output:
            skill_data_per_percentage[student.static_percentage] += (student.hobbit.get_skill() / n)


    plt.plot(skill_data_per_percentage)
    plt.xlabel('Success Percentage')
    plt.ylabel('Skill Level')
    plt.title('Success vs Skill relation. N = ' + str(n))
    plt.grid(True)
    plt.legend().set_visible(False)

    plt.savefig("StudentSkillComparison.png")
    vdisplay.stop()

