import os
import merge_scheduler.merge_scheduler.merge_scheduler
from datetime import date, timedelta
import math
import time
import json
import logging
from collections import defaultdict

log = logging.getLogger()

g = {}


class Job:

    def __init__(self, arg):
        global g
        g = arg

    def start(self):
        global g
        g = {'a': 1}


if __name__ == '__main__':
    with open('./test.json', 'r') as f:
        load = json.load(f)

    # with open('./test.json', 'w') as f:
    #     f.write(json.dumps(load))
    dic1 = defaultdict(list)
    dic1['1'].append(1)
    dic1['1'].append(1)
    dic1['2'].append(2)
    print json.dumps(dic1)

    dic = {}.fromkeys(['a', 'b'], [])
    dic['a'].append(1)
    print dic

    print int(time.mktime(time.strptime('2019-09-13 19:00:00', '%Y-%m-%d %H:%M:%S')) * 1000)
