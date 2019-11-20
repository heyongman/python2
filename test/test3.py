#!/usr/bin/env python
import time
import os
import logging

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = curr_path + os.sep + 'merge_scheduler.log'
LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=LOG_FORMAT)
log = logging.getLogger()
log.addHandler(logging.StreamHandler())

if __name__ == '__main__':
    li = [1, 2, 3]
    for x in range(0,1000000):
        li.append(str(x)+'ejhhgfTTFG')
    print len(li)