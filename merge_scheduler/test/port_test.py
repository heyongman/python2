# coding=utf-8
import socket


def socket_port(ip, port):
    socket.setdefaulttimeout(2)
    """
    输入IP和端口号，扫描判断端口是否占用
    """
    try:
        if port >= 65535:
            print '端口扫描结束'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        if result == 0:
            print ip, ':', port, '端口已占用'
        else:
            print '未被占用'
    except Exception as e:
        print e
        print '端口扫描异常'


if __name__ == '__main__':
    socket_port('127.0.0.1', 9999)
