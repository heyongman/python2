#!/usr/bin/env python
# coding=utf-8
import os
import logging
import shutil
import time
import paramiko
from scp import SCPClient

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(curr_path, "check_target_hz.log")
src_data_dir = "/net_imp/hz"  # 源端数据目录-ftp
src_data_prefix = "zw"  # 源数据文件前缀
dst_data_dir = "/opt/ogg/dirdat/hz/"  # 目标端数据目录-data09
status = 0  # 状态文件的初始值
status_file = os.path.join(curr_path, ".status_hz")
is_first = True
max_no = 999999

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
            logging.error("首次运行可忽略：%s",e)
        logging.info("读取到上次status：%s", status)
        is_first = False

    # 源文件全路径
    src_data_path = os.path.join(src_data_dir, src_data_prefix + str(status).zfill(6))
    next_src_data_path = os.path.join(src_data_dir, src_data_prefix + str(status+1).zfill(6))

    if os.path.exists(src_data_path) & os.path.exists(next_src_data_path):
        # 如果下一个文件已经生成就将上一个文件复制过去
        logging.info("将文件：%s 复制到 %s 成功", src_data_path, dst_data_dir)

        # 将源文件拷贝到目标目录下
        # if not os.path.exists(dst_data_dir):
        #     logging.info("目标目录不存在，即将创建：%s", dst_data_dir)
        #     os.makedirs(dst_data_dir)
        # shutil.copy(src_data_path, dst_data_dir)
        success = ftp_send(src_data_path, dst_data_dir)
        if success:
            # copy完成，状态数+1
            status += 1

        # 如果编号达到了最大值就重置为0
        if status > max_no:
            status = 0

        # 将状态保存到文件
        with open(status_file, "w") as f:
            f.write(str(status))

    else:
        # 否则等待1秒
        time.sleep(1)


def ftp_send(local_path, remote_path):
    host = "104.1.67.216"
    port = 2218
    username = "root"
    password = "Hik@xj2019"
    success = False
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(host, port, username, password)
    scp_client = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)
    try:
        scp_client.put(local_path, remote_path)
    except Exception as e:
        print(e)
        print("系统找不到指定文件" + local_path)
    else:
        success = True
        print("文件上传成功")
    ssh_client.close()
    return success


if __name__ == '__main__':
    while True:
        check()
