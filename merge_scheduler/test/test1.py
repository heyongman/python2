import logging
import os
from logging.handlers import RotatingFileHandler
import test2
import threading

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(curr_path, "test1.log")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

file_handler = RotatingFileHandler(filename=log_path, maxBytes=1024 * 1024 * 10, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

log = logging.getLogger('root')
log.setLevel(logging.DEBUG)
log.addHandler(console_handler)
log.addHandler(file_handler)


class Job:

    def __init__(self,arg):
        self.arg = arg
        print 'init'

    def start(self):
        print 'start'


if __name__ == '__main__':
    log.debug('debug')
    log.info('info')
    log.warn('warn')
    log.error('error')
    gl_arg = {}
    threading.Thread(target=test2.main).start()
    threading.Thread(target=Job(gl_arg).start).start()
