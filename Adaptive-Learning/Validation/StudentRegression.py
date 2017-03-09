__author__ = 'perar'
import simulation_manager as sm
from StudentModel.Student import Student
from StudentModel.BadStudent import BadStudent
from StudentModel.GoodStudent import GoodStudent
from Algorithms.Hobbit.hobbit_sceptical import hobbit_sceptical as hh_sceptical
import multiprocessing
import time
import matplotlib.pyplot as plt

import io
from PIL import Image
import math
import numpy as np
from xvfbwrapper import Xvfb
vdisplay = Xvfb()
vdisplay.start()



def worker(
        x,
        model,
        set_static_percentage=False,
        tasks=100
):

    # Initialize a student
    student = model(id=x)

    #  Set static values if true
    if set_static_percentage:
        student.static = True
        student.static_percentage = x

    #  Init expectation matrix
    student.matrix, student.history_matrix = sm.get_expectation_matrix()
    student.assign_hobbit(hh_sceptical)



    # Request taskset for student
    for x in range(tasks):
        student.request_taskset(num=1)
        answer = student.answer_taskset()
        if answer[0][2]:
            student.winloss["win"] += 1
        else:
            student.winloss["loss"] += 1


        student.deliver_taskset(answer)
        #print(answer, student.hobbit.get_skill())


    # Return student
    return student


def run(num_assignments, num_students):

    student_models = [ Student, BadStudent, GoodStudent]


    model_data = [

    ]

    for model in student_models:
        start_time = time.time()

        pool = multiprocessing.Pool(processes=20)
        results = [pool.apply_async(worker, args=(x, model, False, num_assignments)) for x in range(num_students)]
        output = [p.get() for p in results]

        avg_skill_per_task = []
        avg_win = 0
        avg_loss = 0

        for student in output:
            avg_win += student.winloss["win"]
            avg_loss += student.winloss["loss"]
        avg_win /= len(output)
        avg_loss /= len(output)

        for x in range(num_assignments):
            summen = 0
            for student in output:
                summen += student.history_skill[x]

            avg_skill_per_task.append((summen / num_students) / 10)

        print("Keep These:")
        print("------------------")
        print("%s win %s loss " % (avg_win, avg_loss))
        print("------------------")
        model_data.append({
            "name": model.name.replace("_", ""),
            "data": avg_skill_per_task,
            "winloss": {
                "win": avg_win,
                "loss": avg_loss
            }
        })



    for data in model_data:

        plt.plot(data["data"], label=data["name"])

    print([x["name"] for x in model_data])
    plt.legend([x["name"] for x in model_data], loc='upper left')
    plt.xlabel('Tasks')
    plt.ylabel('Skill Level')

    # ['seaborn-bright',
    # 'fivethirtyeight',
    # 'seaborn-poster',
    # 'seaborn-pastel',
    # 'seaborn-colorblind',
    # 'seaborn-paper',
    # 'seaborn-muted',
    # 'seaborn-dark',
    # 'seaborn-ticks',
    # 'grayscale', 'dark_background', 'seaborn-white', 'seaborn-dark-palette', 'seaborn-whitegrid', 'seaborn-notebook', 'seaborn-darkgrid', 'classic', 'seaborn-deep', 'ggplot', 'seaborn-talk', 'bmh']

    #plt.style.use('ggplot')
    plt.savefig("./Results/Results_s%s_t%s.png" % (num_students, num_assignments))

    plt.clf()










