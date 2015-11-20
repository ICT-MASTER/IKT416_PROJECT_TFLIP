import json
from libs.bottle import static_file
from libs.bottle import route, run, template
from libs.bottle import get, post, request # or route

import hobbit_hood_test
import os
import pickle
import json
import shutil

def generate_student_paths(student):
    student_path = "Students/{0}".format(student)
    tag_path = "{0}/tags.p".format(student_path)
    matrix_path = "{0}/matrix.p".format(student_path)
    taskset_path = "{0}/taskset.p".format(student_path)

    return student_path, tag_path, matrix_path, taskset_path

def load_student(student,
                 tags=True,
                 matrix=True,
                 taskset=True):

    student_path, tag_path, matrix_path, taskset_path = generate_student_paths(student)

    # Load tags
    if tags:
        with open(tag_path, "rb") as file:
            tags = pickle.load(file)

    # Load matrix
    if matrix:
        with open(matrix_path, "rb") as file:
            tags_matrix = pickle.load(file)

    # Load taskset
    if taskset:
        with open(taskset_path, "rb") as file:
            taskset = pickle.load(file)

    return tags, tags_matrix, taskset

def delete_student(student,
                   tags = None,
                   matrix = None,
                   taskset = None,
                   student_dir = None):

    student_path, tag_path, matrix_path, taskset_path = generate_student_paths(student)

    if tags:
        os.remove(tag_path)

    if matrix:
        os.remove(matrix_path)

    if taskset:
        print("Del")
        os.remove(taskset_path)

    if student_dir:
        shutil.rmtree(student_path)

def save_student(student,
                 tags=None,
                 matrix=None,
                 taskset=None):

    student_path, tag_path, matrix_path, taskset_path = generate_student_paths(student)

    # Save tags
    if tags is not None:
        with open(tag_path, "wb") as file:
            file.write(pickle.dumps(tags))

    # Save matrix
    if matrix is not None:
        with open(matrix_path, "wb") as file:
            file.write(pickle.dumps(matrix))

    # Save taskset
    if taskset is not None:
        with open(taskset_path, "wb") as file:
            file.write(pickle.dumps(taskset))




@route('/student/<student>/deliver_taskset', method = "POST")
def deliver_taskset(student):

    taskset = request.json['taskset']

    tags, tags_matrix, old_taskset = load_student(student)

    hobbit_hood_test.evaluate_matrix(tags, tags_matrix, taskset)

    # Save updated matrix
    save_student(student, matrix=tags_matrix)

    # Delete completed taskset
    delete_student(student, taskset=True)

    return json.dumps({
        "tags": tags,
        "matrix": tags_matrix.tolist()
    })



@route('/student/<student>/taskset')
def task_set(student):
    num_tasks = 10

    tags = None
    tags_matrix = None

    try:
        #########################################################
        #
        # Create student directory
        # This happens when a student first requests a taskset
        # * Initialize tags
        # * Initialize matrix
        #
        #########################################################
        student_path = "Students/{0}".format(student)
        tag_path = "{0}/tags.p".format(student_path)
        matrix_path = "{0}/matrix.p".format(student_path)

        # Create student directory
        os.mkdir(student_path)

        # Init student with tags and the tags_matrix
        tags, tags_matrix = hobbit_hood_test.load_tag_matrix()

        # Save tags
        with open(tag_path, "wb") as file:
            file.write(pickle.dumps(tags))

        # Save matrix
        with open(matrix_path, "wb") as file:
            file.write(pickle.dumps(tags_matrix))

    except:
        #########################################################
        #
        # Load tags and tags_matrix from file
        #
        #########################################################
        # Load tags
        with open(tag_path, "rb") as file:
            tags = pickle.load(file)

        # Load matrix
        with open(matrix_path, "rb") as file:
            tags_matrix = pickle.load(file)

    ##############################################
    #
    # Generate taskset which is sent back to the student
    # If a taskset already is sent to the user, return the same taskset without generation
    # * taskset_path: Path to existing taskset
    # * taskset: The loaded taskset
    ##############################################
    taskset_path = "{0}/taskset.p".format(student_path)
    taskset = None
    taskset_is_new = None

    try:
        #######################################
        #
        # Load existing taskset
        #
        #######################################
        file = open(taskset_path, "rb")
        taskset = pickle.load(file)
        file.close()
        taskset_is_new = False
    except FileNotFoundError:
        #######################################
        #
        # Generate new taskset
        #
        #######################################
        taskset = hobbit_hood_test.generate_tasks(tags, tags_matrix, num_tasks, True)
        taskset_is_new = True

        # Save matrix
        with open(matrix_path, "wb") as file:
            file.write(pickle.dumps(tags_matrix))

        # Save taskset
        with open(taskset_path, "wb") as file:
            file.write(pickle.dumps(taskset))

    return json.dumps({
        "is_new": taskset_is_new,
        "taskset": taskset,
        "tags": tags,
        "matrix": tags_matrix.tolist()
    })











if __name__ == "__main__":



    import hobbit_hood_sceptical
    hood = hobbit_hood_sceptical.hobbit_hood_sceptical()





    # Create student directory
    """try:
        os.mkdir("Students")
    except:
        pass

    run(host='0.0.0.0', port=27000)"""

