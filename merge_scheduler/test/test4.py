import time
from flask import Flask, render_template
import merge_scheduler.global_variable as gv
import json
import sys

app = Flask(__name__)


@app.route('/')
# @app.route('/status/<path:path>')
def get_status():
    return json.dumps(gv.get_value())


def start(port):
    print 'start'
    sys.exit(1)
    print 'end'
    app.run(host='0.0.0.0', port=port)
