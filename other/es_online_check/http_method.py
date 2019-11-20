import socket
import urllib
import urllib2
import json


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
            request.add_header('Content-Type', 'json/application')
            response = urllib2.urlopen(request)
            content = response.read()
            if response.code == 200:
                return content, True
            return content, False
        except Exception as ex:
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



