from flask import Flask, request, jsonify, Response
import logging.config
import os
import json

app = Flask(__name__)
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = curr_path + os.sep + 'flask_server.log'
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=LOG_FORMAT)



@app.route('/')
def hello_world():
    log.info('hello')
    return 'Hello!'


@app.route('/register', methods=['POST'])
def register():
    print(request.headers)
    print(request.form)
    # print request.form.get('name', default='default')
    # print request.form.getlist('value')
    return 'welcome'


@app.route('/apps')
@app.route('/apps/<path:path>')
def get_status(path=''):
    # req_dic = request.args
    dic = {"app": {
        "id": path,
        "name": "zs",
        "diagnostics": "Application sfasdds\nsfsdsdf"
    }}
    # return "successCallback"+"("+json.dumps(dic)+")"
    return jsonify([dic['app']])


def start(input_arg):
    # global global_arg
    # global_arg = input_arg
    app.run(port=8080)


if __name__ == '__main__':
    app.run(port=8080)
