#!/usr/bin/env python
# coding=utf-8
import os
import logging
import shutil
import time
import subprocess
import glob

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(curr_path, "check_target_full.log")
src_data_dir = "/net_imp/full_exp"  # 源端数据目录-ftp
dst_data_dir = "/data12/local/full_imp/"  # 目标端数据目录-data09
sleeps = 2

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=log_path, level=logging.INFO, format=LOG_FORMAT)


# log = logging.getLogger()
# log.addHandler(logging.StreamHandler())  # 控制台打印


def check():
    for f in glob.glob('NET_ADMIN*'):
        # 源文件全路径
        src_data_path = os.path.join(src_data_dir, f)
        if os.path.getsize(f) == 52428800:
            logging.info("开始传输：%s", src_data_path)
            success, msg = scp_send(src_data_path, dst_data_dir)
            # success, msg = move(src_data_path, dst_data_dir)
            if success:
                os.remove(src_data_path)
                logging.info("将文件：%s 移动到 %s 成功", src_data_path, dst_data_dir)
            else:
                logging.error("将文件：%s 移动到 %s 失败, 原因：%s", src_data_path, dst_data_dir, msg)
        else:
            # 否则等待5秒
            time.sleep(5)


def scp_send(local_path, remote_path):
    shell = "scp -P 2218 %s root@104.1.67.215:%s" % (local_path, remote_path)
    p = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    w = p.wait()
    # print '执行结果：',w
    if w:
        err = p.stdout.read()
        return False, err
    else:
        out = p.stdout.read()
        return True, out


def move(local_path, remote_path):
    try:
        shutil.move(local_path, remote_path)
        return True, "OK"
    except Exception as e:
        return False, e


if __name__ == '__main__':
    while True:
        check()
        time.sleep(5)
