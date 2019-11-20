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
src_data_dir = "/opt/full_exp"  # 源端数据目录
# src_data_dir = "/root/test1"  # 源端数据目录
src_data_prefix = "NET_ADMIN"  # 源数据文件前缀
src_data_suffix = ".dmp"
dst_data_dir = "/opt/net_exp/full_exp"  # 目标端数据目录
# dst_data_dir = "/root/test2"  # 目标端数据目录
status_file = os.path.join(curr_path, ".status_full")
is_first = True
status = 1  # 状态文件的初始值
sleeps = 2

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=log_path, level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger()
log.addHandler(logging.StreamHandler())  # 控制台打印

# 1 按顺序将文件切分，记录20G文件编号
# 2 将一个20G文件切分的100个文件按顺序等待并移动到摆渡目录
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
    src_data_path = os.path.join(src_data_dir, src_data_prefix + str(status).zfill(2) + src_data_suffix)
    next_src_data_path = os.path.join(src_data_dir, src_data_prefix + str(status+1).zfill(2) + src_data_suffix)

    if os.path.exists(src_data_path) & os.path.exists(next_src_data_path):
        logging.info('检测到新的文件： %s', src_data_path)
        # 创建拆分文件的目录
        curr_split_dir = os.path.join(src_data_dir, src_data_prefix + str(status).zfill(2))
        # 拆分文件前缀
        split_prefix = src_data_prefix + str(status).zfill(2) + '_PART_'
        if os.path.isdir(curr_split_dir):
            # 如果拆分目录已存在，就继续传
            os.chdir(curr_split_dir)
        else:
            # 如果拆分目录不存在，就创建目录，拆分文件，然后传
            os.mkdir(curr_split_dir)
            os.chdir(curr_split_dir)
            split_file(src_data_path, split_prefix)
            # 拆分成功把源文件删除!!
            os.remove(src_data_path)
        
        # 拆分成功后就将小文件逐个放入摆渡
        split_files = glob.glob(split_prefix+'*')
        split_files.sort(key=lambda x: int(x[len(split_prefix):]))
        logging.info('当前传输的拆分文件列表： %s', split_files)

        for file in split_files:
            # 判断摆渡目录是否还有文件，有就等待
            dst_file_prefix = os.path.join(dst_data_dir, src_data_prefix+'*')
            while len(glob.glob(dst_file_prefix)) > 0:
                time.sleep(5)
            
            # 开始传文件
            success = move(file, dst_data_dir)
        
        # 当前拆分文件移动完毕
        status += 1
        # 将状态保存到文件
        with open(status_file, "w") as f:
            f.write(str(status))
        logging.info('新的状态保存成功： status: %s', status)


def split_file(src_data_path, split_prefix):
    shell = 'split -d -b 50m %s %s' % (src_data_path, split_prefix)
    logging.info('即将执行拆分文件命令：%s', shell)
    p = subprocess.Popen(shell,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    w = p.wait()
    if w:
        err = p.stderr.read()
        logging.error('文件拆分失败,程序停止！')
        sys.exit(1)
    else:
        out = p.stdout.read()
        logging.info('文件拆分成功。')

def scp_send(local_path, remote_path):
    shell = "scp -P 2218 %s root@104.1.67.215:%s" % (local_path, remote_path)
    p = subprocess.Popen(shell,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    w = p.wait()
    # print '执行结果：',w
    if w:
        err = p.stderr.read()
        return False, err
    else:
        out = p.stdout.read()
        os.remove(src_data_path)
        return True,out

def move(local_path, remote_path):
    # global sleeps
    try:
        shutil.move(local_path, remote_path)
        logging.info("将文件：%s 移动到 %s 成功", local_path, remote_path)
        sleeps = 2
        return True
    except Exception as e:
        logging.error("将文件：%s 移动到 %s 失败! 失败原因：%s", local_path, remote_path, e)
        sleeps = sleeps * sleeps
        logging.info(" %s 秒后重试。", sleeps)
        time.sleep(sleeps)
        return False
    

if __name__ == '__main__':
    while True:
        check()
        time.sleep(5)
