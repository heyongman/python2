#!/usr/bin/env python
# coding=utf-8
import os
import logging
import shutil
import time
import subprocess
import glob
import sys

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(curr_path, "check_source_full.log")
src_data_dir = "/opt/full_exp/"  # 源端数据目录
# src_data_dir = "/root/test1"  # 源端数据目录
src_data_prefix = "NET_ADMIN"  # 源数据文件前缀
src_data_suffix = ".dmp"
dst_data_dir = "/opt/net_exp/full_exp/"  # 目标端数据目录
# dst_data_dir = "/root/test2"  # 目标端数据目录
start_file = ''
using_file = ['*']


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=log_path, level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger()
log.addHandler(logging.StreamHandler())  # 控制台打印


# 1 按顺序将文件切分
# 2 将一个20G文件切分的400个文件按顺序等待并移动到摆渡目录
def check():
    if start_file == '':
        flag = True
    else:
        flag = False
    indexes = [1, 2, 3]
    for status in range(1, 5):
        # 源文件全路径
        src_data_path = os.path.join(src_data_dir, src_data_prefix + str(status).zfill(2) + src_data_suffix)
        # 创建拆分文件的目录
        curr_split_dir = os.path.join(src_data_dir, src_data_prefix + str(status).zfill(2))
        # 拆分文件前缀
        split_prefix = src_data_prefix + str(status).zfill(2) + '_PART_'
        if os.path.isdir(curr_split_dir):
            logging.info('检测到已有的拆分目录： %s', curr_split_dir)
            # 如果拆分目录已存在，就继续传
            os.chdir(curr_split_dir)
        elif os.path.exists(src_data_path):
            logging.info('检测到新的文件： %s', src_data_path)
            # 如果拆分目录不存在，就创建目录，拆分文件，然后传
            os.mkdir(curr_split_dir)
            os.chdir(curr_split_dir)
            split_file(src_data_path, split_prefix)
            # 拆分成功把源文件删除!!
            try:
                os.remove(src_data_path)
            except Exception as e:
                logging.exception(e)

        # 拆分成功后就将小文件逐个放入摆渡
        split_files = glob.glob(split_prefix + '*')
        split_files.sort(key=lambda x: int(x[len(split_prefix):]))
        # logging.info('当前传输的拆分文件列表： %s', split_files)

        for split in split_files:
            # 判断摆渡目录是否还有文件，有就等待
            dst_file_prefix = os.path.join(dst_data_dir, src_data_prefix + '*')
            src_split_path = os.path.join(curr_split_dir, split)
            while len(glob.glob(dst_file_prefix)) > 0:
                time.sleep(5)
            # 从start_file开始传输
            if split == start_file:
                flag = True
            if not flag:
                continue
            if using_file[0] == '*' or split in using_file:
                # 开始传文件
                success = copy(src_split_path, dst_data_dir)


def split_file(src_data_path, split_prefix):
    shell = 'split -d -b 50m %s %s' % (src_data_path, split_prefix)
    logging.info('即将执行拆分文件命令：%s', shell)
    p = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    w = p.wait()
    out = p.stdout.read()
    if w:
        logging.error('文件拆分失败,程序停止！\n%s', out)
        sys.exit(1)
    else:
        logging.info('文件拆分成功。')


def copy(local_path, remote_path):
    try:
        if os.path.isdir(remote_path):
            remote_path = os.path.join(remote_path, os.path.basename(local_path))
        shutil.copyfile(local_path, remote_path)
        logging.info("将文件：%s 复制到 %s 成功", local_path, remote_path)
        return True
    except Exception as e:
        logging.exception("将文件：%s 复制到 %s 失败! 失败原因：%s", local_path, remote_path, e)


if __name__ == '__main__':
    check()
