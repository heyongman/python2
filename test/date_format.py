# coding=utf-8
import time
import datetime

if __name__ == '__main__':
    # timestamp to datetime
    t1 = time.localtime(1568377139)
    print t1

    t2 = time.strftime('%Y-%m-%d %H:%M:%S', t1)
    print t2

    t3 = time.strptime('2019-09-13 19:00:00', '%Y-%m-%d %H:%M:%S')
    print t3

    t4 = time.mktime(t3)*1000
    print int(t4)

    t5 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    print t5

    t = time.time()

    print (t)  # 原始时间数据
    print (int(t))  # 秒级时间戳
    print (int(round(t * 1000)))  # 毫秒级时间戳
    print (int(round(t * 1000000)))  # 微秒级时间戳
