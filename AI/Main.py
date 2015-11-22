import Student_Create
import Student_Clean
import StudentEngine
import json
import requests as req
from libs.bottle import static_file
from libs.bottle import route, run, template
from libs.bottle import get, post, request # or route




@route('/<filename>')
def server_static(filename):
    return static_file(filename, root='./public_html')

@route('/api/students')
def students():
    pass

@route('/api/clean_students')
def clean_students():
    Student_Clean.clean()
    return json.dumps({
        'message': "OK"
    })


@route('/api/student/deliver_taskset', method='POST')
def deliver_taskset():
    name = request.json["name"]
    taskset = request.json["taskset"]

    data = req.post("http://localhost:27000/student/" + name + "/deliver_taskset", json={
        'taskset': taskset
    })

    print(data)
    return data.json()




@route('/api/student/<student>/taskset')
def taskset(student):

    data = req.get("http://localhost:27000/student/{0}/taskset".format(student))
    return data.json()



@route('/api/students')
def create_students():
    return json.dumps(StudentEngine.get_students())

@route('/api/create_students')
def create_students():
    Student_Create.generate()


    return json.dumps({
        'message': "OK",
        'students': StudentEngine.get_students()
    })










if __name__ == "__main__":
    run(host='0.0.0.0', port=8080)

