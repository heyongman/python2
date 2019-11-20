#!/usr/bin/env python
# coding=utf-8
import os
import logging
import shutil
import time
import subprocess

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(curr_path, "check_target_nd.log")
src_data_dir = "/net_imp/nd"  # 源端数据目录-ftp
src_data_prefix = "zw"  # 源数据文件前缀
dst_data_dir = "/opt/ogg/dirdat/nd/"  # 目标端数据目录-data09
status = 0  # 状态文件的初始值
status_file = os.path.join(curr_path, ".status_nd")
is_first = True
max_no = 999999
sleeps = 2

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=log_path, level=logging.INFO, format=LOG_FORMAT)
# log = logging.getLogger()
# log.addHandler(logging.StreamHandler())  # 控制台打印


def check():
    # 重启后加载状态文件
    global is_first
    if is_first:
        try:
            with open(status_file, "r") as f:
                global status
                status = int(f.readline())
        except Exception as e:
            pass
            # logging.error("首次运行可忽略：%s",e)
        logging.info("读取到上次status：%s", status)
        is_first = False

    # 源文件全路径
    src_data_path = os.path.join(src_data_dir, src_data_prefix + str(status).zfill(6))
    next_src_data_path = os.path.join(src_data_dir, src_data_prefix + str(status+1).zfill(6))

    if os.path.exists(src_data_path) & os.path.exists(next_src_data_path):
        # 如果下一个文件已经生成就将上一个文件复制过去
        success, msg = scp_send(src_data_path, dst_data_dir)
        global sleeps
        if success:
            # copy完成，状态数+1
            status += 1
            os.remove(src_data_path)
            logging.info("将文件：%s 移动到 %s 成功", src_data_path, dst_data_dir)
            sleeps = 2
        else:
            logging.error("将文件：%s 移动到 %s 失败, 原因：%s", src_data_path, dst_data_dir, msg)
            sleeps = sleeps * sleeps
            logging.info(" %s 秒后重试。", sleeps)
            time.sleep(sleeps)

        # 如果编号达到了最大值就重置为0
        if status > max_no:
            status = 0

        # 将状态保存到文件
        with open(status_file, "w") as f:
            f.write(str(status))

    else:
        # 否则等待1秒
        time.sleep(1)


def scp_send(local_path, remote_path):
    shell = "scp -P 2218 %s root@104.1.67.216:%s" % (local_path, remote_path)
    p = subprocess.Popen(shell,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    w = p.wait()
    # print '执行结果：',w
    if w:
        err = p.stderr.read()
        return False, err
    else:
        out = p.stdout.read()
        return True,out



if __name__ == '__main__':
    while True:
        check()
