#!/usr/bin/env python
# coding=utf-8
import json
import logging
import os

from flask import Flask, render_template, url_for, redirect

import global_variable as gv
import http_method

curr_path = os.path.dirname(os.path.abspath(__file__))
app_ids_path = '/root/merge_scheduler/merge/appid_zg_zd.json'

app = Flask(__name__)

log = logging.getLogger('ConsoleFileLogger')


@app.route('/')
def hello_world():
    # return render_template('demo.html')
    res_list = [{'table': 'zg_zd.hive-1', 'app_id': 'application_1', 'hdfs_path': '/ogg/1', 'status': 'SUCCEEDED'},
                {'table': 'zg_zd.hive-2', 'app_id': 'application_2', 'hdfs_path': '/ogg/2', 'status': 'UNDEFINED'},
                {'table': 'zg_zd.hive-3', 'app_id': 'application_3', 'hdfs_path': '/ogg/3', 'status': 'FAILED'},
                {'table': 'zg_zd.hive-4', 'app_id': 'application_4', 'hdfs_path': '/ogg/4', 'status': 'SUCCEEDED'}
                ]

    res_list = json.dumps(res_list)
    # print res_list
    return render_template('home.html')
    # return render_template('demo.html')


@app.route('/status')
def get_status():
    id_status = http_method.get_app_status()
    for config in gv.get_value():
        config['status'] = id_status.get(config.get('app_id'))
        # config['status'] = 'SUCCEEDED'

    return render_template('merge.html', res_list=json.dumps(gv.get_value()))


@app.route('/app_info/<path:app_id>')
def get_app_info(app_id=''):
    if app_id == '' or app_id == 'undefined':
        return 'no results found.'
    res = http_method.get_app_info(app_id)
    return res


@app.route('/init')
def init():
    gv.init()
    with open(app_ids_path, 'r') as f:
        gv.set_value(json.load(f))
    print gv.get_value()[:3]
    return redirect(url_for('get_status'))


@app.route('/test')
def test():
    return render_template('demo2.html')


def start(port):
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
