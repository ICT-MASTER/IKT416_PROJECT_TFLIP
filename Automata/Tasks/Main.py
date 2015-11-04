__author__ = 'perar'

import json

from bottle import route, run

from Automata import TaskGenerator


@route('/tasks/list')
def index():
    return "<pre>" + json.dumps(TaskGenerator.load(), sort_keys=True, indent=4, separators=(',', ': ')) + "</pre>"

@route('/homo')
def penis():
    return "<pre>"+ "NATTEN.HOMO.IT"+"</pre>"







if __name__ == '__main__':

    run(host='localhost', port=8080)
