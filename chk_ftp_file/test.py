# coding=utf-8
import logging
import os
import traceback
import time
import hashlib
import shutil

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(curr_path, "test.log1")
status_file = os.path.join(curr_path, ".status1")
src_file = os.path.join(curr_path, "src", "zd000000")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s - %(lineno)d"
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=LOG_FORMAT)
log = logging.getLogger()
log.addHandler(logging.StreamHandler())

status = 0


# 计算md5
def cert_util(file_path, n=4096):
    md5_1 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(n)
            if data:
                md5_1.update(data)
            else:
                break
    ret = md5_1.hexdigest()
    return ret


def method():
    os.chdir('C:\\proj-20190610\\proj\\py_proj')
    print os.getcwd()


if __name__ == '__main__':
    method()
