import os
import logging
import test2
import threading

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = curr_path + os.sep + 'test3.log'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(threadName)s - %(message)s"
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=LOG_FORMAT)

console = logging.StreamHandler()
console.setLevel('INFO')
console.setFormatter(logging.Formatter(LOG_FORMAT))
logging.getLogger().addHandler(console)


def loop():
    logging.info('loop info')


if __name__ == '__main__':
    logging.debug('debug')
    logging.info('info')
    logging.warn('warn')
    logging.error('error')

    test2.main()

    t = threading.Thread(target=loop)
    t.start()
