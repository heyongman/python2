#!/usr/bin/env python
import threading
import os
import time
import sys


def loop():
    while True:
        print threading.current_thread().ident
        time.sleep(3)
        sys.exit(1)


if __name__ == '__main__':
    t1 = threading.Thread(target=loop)
    # t1.setDaemon(True)
    t1.start()
    t2 = threading.Thread(target=loop)
    # t2.setDaemon(True)
    t2.start()
    while True:
        print 'q'
        time.sleep(1)
