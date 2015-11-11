__author__ = 'perar'

from bottle import route, run, template
from Automata.Generator.TaskGenerator import TaskGenerator
import json

@route('/tasks/list')
def index():
    return "<pre>" + json.dumps(TaskGenerator.load(), sort_keys=True, indent=4, separators=(',', ': ')) + "</pre>"



if __name__ == '__main__':
    run(host='localhost', port=8080)
