import time
import json
from datetime import date, timedelta, datetime
import math
import urllib2

from fnmatch import fnmatch, fnmatchcase


def test():
    yesterday = date.today() + timedelta(days=-1)
    print str(yesterday)
    start_time = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')) * 1000)
    print start_time


def test1():
    inc_size = 0.080
    print math.ceil(1 + inc_size * 18), 1 + inc_size * 18
    print math.ceil(1 + inc_size * 5), 1 + inc_size * 5
    print round(1 + (inc_size - 0.001) * 4), 1 + (inc_size - 0.001) * 4
    print round(1 + (inc_size - 0.001) * 15), 1 + (inc_size - 0.001) * 15


def test2():
    try:
        req = urllib2.Request('http://www.baiduw.com/sedwe/we')
        ret = urllib2.urlopen(req)
    except Exception as e:
        print e
        print '404' in str(e)


def test3():
    s1 = '2019-09-28'
    # before_time = time.strptime(s1, '%Y-%m-%d')
    before_time = datetime.strptime(s1, '%Y-%m-%d')
    now = datetime.today()
    print before_time, now
    before_days = -(now - before_time).days
    print before_days


def test4():
    inc_tab = set()
    inc_tab.add(('zg_zd.hive_vio_log', 'TRFF_APP.VIO_LOG'))
    inc_tab.add(('zg_zd.hive_vio_log1', 'TRFF_APP.VIO_LOG'))
    restore_tb = []
    restore_tb.append('zg_zd.hive_vio_log')
    if restore_tb:
        print 'not null'
    filtered = filter(lambda (tb, ori): tb in restore_tb, inc_tab)
    print filtered


def test5():
    if test6():
        print 'true'
    else:
        print 'false'


def test6():
    return False


if __name__ == '__main__':
    test1()
