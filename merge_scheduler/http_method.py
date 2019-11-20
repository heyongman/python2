import json
import logging
import socket
import time
import urllib2
from datetime import date, timedelta

log = logging.getLogger('ConsoleFileLogger')


def get(url):
    try:
        req = urllib2.Request(url)
        ret = urllib2.urlopen(req)
        return json.load(ret)
    except Exception as ex:
        if '404' in str(ex):
            log.warn('Http get error, url: %s, cause: %s', url, ex)
        else:
            log.error('Http get error, url: %s, cause: %s', url, ex)


def get_app_status(before_days=-1):
    # return id:status dic
    app_name = 'merge_scheduler'
    # app_name = 'merge'
    yesterday = date.today() + timedelta(days=before_days)
    start_time = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')) * 1000)
    # start_time = int(time.mktime(time.strptime('2019-09-13 19:00:00', '%Y-%m-%d %H:%M:%S')) * 1000)
    yarn_list_url = 'http://104.1.67.206:18088/ws/v1/cluster/apps/?startedTimeBegin=%s' % start_time
    res = get(yarn_list_url)
    if res is None:
        return {}
    app_list = res['apps']['app']
    id_status = {}
    for app_info in app_list:
        if not app_info['name'] == app_name:
            continue
        id_status[app_info['id']] = app_info['finalStatus']
    return id_status


def get_app_info(app_id):
    # return 'fsdfsd:\n\t%s' % app_id
    url = 'http://104.1.67.206:18088/ws/v1/cluster/apps/%s' % app_id
    res = get(url)
    if res is None or res.get('app').get('diagnostics') == '':
        return 'no results found.'
    return res.get('app').get('diagnostics')


def get_hdfs_info(hdfs_path):
    webhdfs_list_url = 'http://104.1.67.206:50070/webhdfs/v1%s?op=LISTSTATUS'
    response = get(webhdfs_list_url % hdfs_path)
    if response is None:
        return []
    return response.get('FileStatuses').get('FileStatus')


def port_detection(ip, port):
    socket.setdefaulttimeout(2)
    try:
        if port >= 65535:
            return
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        if result == 0:
            return True
        else:
            return False
    except Exception as e:
        log.error('Detection port occupation error:%s', e)
