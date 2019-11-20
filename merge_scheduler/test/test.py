#!/usr/bin/env python
import time
import json
import os
import subprocess
import logging
import shutil
from datetime import datetime,date,timedelta
import SimpleHTTPServer

import atexit
import os
import sys
import time
import platform
import shutil
import traceback
from datetime import datetime

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = curr_path + os.sep + 'test.log'
LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename=log_path, level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger()
log.addHandler(logging.StreamHandler())


def test1():
    s = '''
        {
          "FileStatuses":
          {
            "FileStatus":
            [
              {
                "accessTime"      : 1320171722771,
                "blockSize"       : 33554432,
                "group"           : "supergroup",
                "length"          : 24930,
                "modificationTime": 1320171722771,
                "owner"           : "webuser",
                "pathSuffix"      : "a.patch",
                "permission"      : "644",
                "replication"     : 1,
                "type"            : "FILE"
              },
              {
                "accessTime"      : 0,
                "blockSize"       : 0,
                "group"           : "supergroup",
                "length"          : 0,
                "modificationTime": 1320895981256,
                "owner"           : "username",
                "pathSuffix"      : "bar",
                "permission"      : "711",
                "replication"     : 0,
                "type"            : "DIRECTORY"
              }
            ]
          }
        }
    '''

    s_j = json.loads(s)
    li = []
    li.extend([3, 4, None])
    # li = filter(None, li)
    print li
    print map(lambda x: x.get('pathSuffix'), s_j.get('FileStatuses').get('FileStatus'))


def test2():
    li1 = [1, 2, 3]
    li2 = [4, 5, 6]
    li3 = zip(li1, li2)
    li1.extend(map(lambda x: (x, 'a'), range(3)))
    print li1


def test3():
    head, sep, tail = 'trff_appersw49rfwe'.partition('.')
    print '[%s],[%s],[%s]' % (head, sep, tail)
    if not None:
        print "not enpty"


def test4():
    os.chdir('/mnt/c/Users/Administrator/Downloads/Programs/navicat')
    p = subprocess.Popen(
        'split -d -b 10m /mnt/c/Users/Administrator/Downloads/Programs/navicat121_premium_cs_x64.exe navi_part_',
        shell=True)
    res = p.wait()
    print res


def test5():
    try:
        1 / 0
    except Exception as e:
        logging.exception('Error msg.\n%s', e)
        logging.info('-------------------------')
        logging.error('Error msg.\n%s', e)


def test6():
    shell = 'C:\\Soft\\Python-2.7.13.1\\python-2.7.13.amd64\\python.exe C:\\proj-20190610\\proj\\py_proj\\python2\\test\\test3.py'
    p = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with p.stdout:
        while p.poll() is None:
            for line in iter(p.stdout.readline, b''):
                # if not p.poll() is None:
                #     break
                print line,
        print p.poll()
    # ret = p.wait()
    print p.returncode
    # print ret


def test7():
    task_config = {}
    task_config['zg_zd.vio_log'] = {'app_id': 'application_231'}
    task_config['zg_zd.sfe_fsd'] = {'app_id': 'application_654'}
    for k, v in task_config.items():
        task_config[k]['config'] = '/ogg/R_ZG_ZD/2019-09-08_*/TRFF_APP.VIO_LOG-*' + k

    print task_config


def test8():
    a = '''
        spark-submit --class com.he.Test \\\
        --master yarn \\\
        --deploy-mode cluster \\\
        --driver-memory 1G \\\
        --executor-memory 4G \\\
        --executor-cores 2 \\\
        --num-executors 4 \\\
        --name merge \\\
        test.jar "%s" "%s"
        '''

    last_ymd = (date.today() + timedelta(days=-1)).strftime('%Y-%m-%d')
    print last_ymd
    dic = {'a': {'aa':'a1'},'b': {'bb': 'b1'}}
    print dic.items()[:3]


if __name__ == '__main__':
    test8()
