import json
from libs.bottle import static_file
from libs.bottle import route, run, template
from libs.bottle import get, post, request # or route

from hobbit_hood_sceptical import hobbit_hood_sceptical
import os
import pickle
import json

def load_student(student):
    student_path = "Students/{0}.p".format(student)
    try:
        with open(student_path, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        hobbit_hood = hobbit_hood_sceptical()
        save_student(student, hobbit_hood)
        return hobbit_hood


def delete_student(student):
    student_path = "Students/{0}.p".format(student)
    os.remove(student_path)


def save_student(student, hobbit_hood):
    student_path = "Students/{0}.p".format(student)
    with open(student_path, "wb") as file:
        file.write(pickle.dumps(hobbit_hood))



@route('/student/<student>/deliver_taskset', method = "POST")
def deliver_taskset(student):

    taskset = request.json['taskset']

    hobbit_hood = load_student(student)

    hobbit_hood.evaluate_taskset(taskset)

    # Save updated matrix
    save_student(student, hobbit_hood)

    return json.dumps({
        "tags": hobbit_hood.categories,
        "matrix": hobbit_hood.matrix.tolist()
    })



@route('/student/<student>/taskset')
def task_set(student):

    hobbit_hood = load_student(student)

    hobbit_hood.generate_taskset()

    return json.dumps({
        "taskset": hobbit_hood.taskset,
        "tags": hobbit_hood.categories,
        "matrix": hobbit_hood.matrix.tolist()
    })











if __name__ == "__main__":




    # Create student directory
    try:
        os.mkdir("Students")
    except:
        pass

    run(host='0.0.0.0', port=27000)

