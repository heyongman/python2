# coding=utf-8
from __future__ import unicode_literals
import sys
import os
import logging
import urllib
import urllib2
import json
from elasticsearch import Elasticsearch
import csv
import json
import re

sys_type = sys.getfilesystemencoding()

curr_path = os.path.dirname(os.path.abspath(__file__))
# data_file_path = os.path.join(curr_path, 'data')

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename=curr_path + os.sep + 'increment_table_check.log', level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger()
log.addHandler(logging.StreamHandler())  # 控制台打印


class ES:
    def __init__(self):
        self.es = Elasticsearch(hosts="http://192.168.21.33:9200/", http_auth=('abc', 'dataanalysis'))
        print(self.es.info())

    def get(self):
        query = {}
        res = self.es.search(index='', body=query)
        total = res['hits']['total']
        print total


def get(url):
    try:
        en_data = urllib.urlencode({"wd": "python"})
        header = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
            'Content-Type': 'application/json'
        }
        # header = {}
        url += en_data
        print url
        request = urllib2.Request(url=url, headers=header)
        response = urllib2.urlopen(request, timeout=10)
        return response.read()
    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    # ES()
    s = u'手動a'
    s1 = s.encode('utf-8')

