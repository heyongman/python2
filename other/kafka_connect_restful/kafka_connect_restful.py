#!/usr/bin/env python
# coding=utf-8
from optparse import OptionParser
from optparse import OptionGroup
import sys
import urllib
import urllib2
import json
import socket
import traceback


class HttpMethod(object):

    def __init__(self):
        pass

    @staticmethod
    def post(url=None, params=None, timeout=50):
        """Post方法"""
        old_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        try:
            # POST
            if params:
                request = urllib2.Request(url, urllib.urlencode(params))
            # GET
            else:
                request = urllib2.Request(url)
            # request.add_header('Accept-Language', 'zh-cn')
            # request.add_header('Content-Type', 'json/application')
            response = urllib2.urlopen(request)
            content = response.read()
            if response.code == 200:
                return content, True
            return content, False
        except Exception as ex:
            print traceback.format_exc()
            print ("Post 方法调用异常：%s" % ex)
            return str(ex), False
        finally:
            if 'response' in dir():
                response.close()
            socket.setdefaulttimeout(old_timeout)

    @staticmethod
    def put(url=None, params=None, url_encode=True):
        """urlencode 表明参数是否需要被编码,如果此选项为false。传入的params 需要是字符串形式"""
        try:
            if url_encode:
                data = urllib.urlencode(params)
            else:
                data = params
            req = urllib2.Request(url, data)
            req.get_method = lambda: 'PUT'
            ret = urllib2.urlopen(req).read()
            return ret
        except Exception as ex:
            print("Put方法调用异常：%s" % ex)

    @staticmethod
    def get(url):
        """get方法"""
        try:
            req = urllib2.Request(url)
            ret = urllib2.urlopen(req)
            return json.load(ret)
        except Exception as ex:
            print("Get方法调用异常：%s" % ex)

    @staticmethod
    def delete(url=None, params=None):
        """定义delete 方法"""
        try:
            data = urllib.urlencode(params)
            req = urllib2.Request(url, data)
            req.get_method = lambda: 'DELETE'
            ret = urllib2.urlopen(req).read()
            return ret
        except Exception as ex:
            print("Delete 方法调用异常：%s" % ex)


def execute(url):
    parser = get_option_parser()
    options, args = parser.parse_args(sys.argv[1:])
    print options, args
    if options.postParam:
        url = url + 'register'
        with open(options.postParam, 'r') as f:
            for line in f:
                json_line = json.loads(line, encoding='utf-8')
                res, stat = HttpMethod.post(url=url, params=json_line)
                print res, stat
    elif options.resumeParam:
        pass
    elif options.pauseParam:
        pass
    elif options.startParam:
        pass
    elif options.startParam:
        pass
    else:
        print 'Options cannot be recognized, try type -h to get help.'


def get_option_parser():
    usage = "usage: %prog options [config-path]"
    parser = OptionParser(usage=usage)

    option_group = OptionGroup(parser, "Program Options")
    option_group.add_option("-c", metavar="<create connector using config file>", dest="postParam", action="store",
                            help="JSON inline format config ")
    option_group.add_option("-r", metavar="<resume a paused connector>", dest="resumeParam", action="store",
                            help="* means resume all connector")
    option_group.add_option("-p", metavar="<pause a paused connector>", dest="pauseParam", action="store",
                            help="* means pause all connector")
    option_group.add_option("-s", metavar="<start worker>", dest="startParam", action="store_true", help="start worker")
    option_group.add_option("-k", metavar="<pause all connector and stop worker>", dest="killParam",
                            action="store_true", help="pause all connector and stop worker")
    parser.add_option_group(option_group)
    return parser


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    base_url = 'http://127.0.0.1:5000/'
    execute(base_url)
