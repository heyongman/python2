import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import test2
import time

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(curr_path, "test1.log")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

time_rotating_handler = TimedRotatingFileHandler(filename=log_path, when='d', interval=1, backupCount=5, encoding='utf-8')
time_rotating_handler.setLevel(logging.DEBUG)
time_rotating_handler.setFormatter(logging.Formatter(LOG_FORMAT))
# file_handler = RotatingFileHandler(filename=log_path, maxBytes=1024*1024*10, encoding='utf-8')
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

log = logging.getLogger('test1')
log.setLevel(logging.DEBUG)
log.addHandler(console_handler)
# log.addHandler(file_handler)
log.addHandler(time_rotating_handler)

if __name__ == '__main__':
    while True:
        log.debug('debug')
        log.info('info')
        log.warn('warn')
        log.error('error')

        test2.main()

        time.sleep(5)
