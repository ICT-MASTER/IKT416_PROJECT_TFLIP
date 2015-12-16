__author__ = 'perar'
from Algorithms.Hobbit.hobbit_sceptical import hobbit_sceptical as hh_sceptical
import simulation_manager as sm
from Student import Student
import matplotlib.pyplot as plt
import multiprocessing
import time

num_iterations = 100
num_assignments = 10

# PLOT DATA
history_data = []

# Student
student = Student(id=-1)
student.assign_hobbit(hh_sceptical)

def worker(x):
    print("{0} of {1} | ({2}%)".format(x, num_iterations, (x/num_iterations)*100.0))
    student = Student(id=x, static=True, static_percentage=70)
    student.matrix, student.history_matrix = sm.get_expectation_matrix()
    student.assign_hobbit(hh_sceptical)

    for y in range(num_assignments):
        student.request_taskset()
        answer = student.answer_taskset()
        student.deliver_taskset(answer)


    return student.history_matrix

if __name__ == '__main__':

    startTime = time.time()
    jobs = []
    pool = multiprocessing.Pool(processes=7)
    results = [pool.apply_async(worker, args=(x,)) for x in range(num_iterations)]
    output = [p.get() for p in results]

    for item in output:
        history_data.append(item)



    print("Took {0} seconds to execute {1} iterations".format(time.time() - startTime, num_iterations))

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
        legend = ax.legend(loc='upper right', shadow=True)


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
        buf.seek(0)
        im = Image.open(buf)
        images.append(im)



    width, height = images[0].size

    num_cols = 3
    num_rows = math.ceil(len(images) / 3.0)

    img_width = width * 3  # 3 Columns
    img_height = num_rows * height  # Num rows

    new_im = Image.new('RGB', (img_width, img_height))


    count = 0
    for row in range(0, img_height, height):
        for col in range(0, img_width, width):
            try:
                new_im.paste(images[count], (col, row))
            except: pass

            count += 1

    new_im.save("summary.png")
    new_im.show()




    """
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
    """

