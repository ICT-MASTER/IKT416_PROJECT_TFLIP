import Student_Create
import Student_Clean
import StudentEngine
import json
from libs.bottle import static_file
from libs.bottle import route, run, template




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

