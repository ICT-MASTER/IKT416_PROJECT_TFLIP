__author__ = 'perar'
import simulation_manager as sm
from StudentModel.Student import Student
from StudentModel.BadStudent import BadStudent
from StudentModel.GoodStudent import GoodStudent
from Algorithms.Hobbit.hobbit_sceptical import hobbit_sceptical as hh_sceptical
import multiprocessing
import time
import matplotlib.pyplot as plt





def worker(
        x,
        model,
        set_static_percentage=False,
        no_output=False,
        num_students=10,
        num_assignments=10,
        epsilon=.0
):
    # Omit output if true
    if not no_output:
        print("{0} of {1} | ({2}%)".format(x, num_students, (x/num_students)*100.0))

    # Initialize a student
    student = model(id=x, static_epsilon=True )
    student.epsilon = epsilon

    #  Set static values if true
    if set_static_percentage:
        student.static = True
        student.static_percentage = x

    #  Init expectation matrix
    student.matrix, student.history_matrix = sm.get_expectation_matrix()
    student.assign_hobbit(hh_sceptical)

    # Request taskset for student
    for y in range(num_assignments):
        student.request_taskset()
        answer = student.answer_taskset()
        student.deliver_taskset(answer)

    # Return student
    return student


def run(num_assignments, num_students, epsilon):

    history_data = []
    student_models = [Student]



    for model in student_models:
        history_data.clear()

        start_time = time.time()
        pool = multiprocessing.Pool(processes=7)
        results = [pool.apply_async(worker, args=(x,model, False, False, num_students, num_assignments, epsilon)) for x in range(num_students)]
        output = [p.get() for p in results]

        for student in output:
            history_data.append(student.history_matrix)



        print("Took {0} seconds to execute {1} iterations".format(time.time() - start_time, num_students))

        # Compile history
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




        charts = []
        for x in range(len(history[0])):
            fig, ax = plt.subplots()
            charts.append((fig, ax))


        for x in range(len(history)):
            for y_line in range(len(history[x])):

                fig, ax = charts[y_line]
                ax.plot(history[x][y_line], label="{0} - {1}".format(student.hobbit.categories[x], y_line))

        for x in range(len(charts)):
            fig, ax = charts[x]
            # Now add the legend with some customizations.
            legend = ax.legend(loc='upper left', shadow=True)


            # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
            frame = legend.get_frame()
            frame.set_facecolor('0.90')
            # Set the fontsize
            for label in legend.get_texts():
                label.set_fontsize('large')

            for label in legend.get_lines():
                label.set_linewidth(1.5)  # the legend line width


        import io
        from PIL import Image
        import math

        # Save all figures to file
        images = []
        for x in range(len(charts)):
            fig, ax = charts[x]
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            fig.savefig("./Results/Static_Epsilon_" + str(epsilon) + "_" + str(x) + "_summary.eps", format='eps', dpi=1000)
            buf.seek(0)
            im = Image.open(buf)
            images.append(im)



        width, height = images[0].size

        num_cols = 3
        num_rows = math.ceil(len(images) / 3.0)

        img_width = width * 3  # 3 Columns
        img_height = num_rows * height  # Num rows

        new_im = Image.new('RGBA', (img_width, img_height))


        count = 0
        for row in range(0, img_height, height):
            for col in range(0, img_width, width):
                try:
                    new_im.paste(images[count], (col, row))
                except: pass

                count += 1

        new_im.save("./Results/Static_Epsilon_" + str(epsilon) + "_summary.png")