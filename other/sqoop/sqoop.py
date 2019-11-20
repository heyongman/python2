#!/usr/bin/env python
# coding=utf-8
import os
import subprocess
import logging
import time

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(curr_path, "sqoop_python.log")

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=LOG_FORMAT)


def compute_table():
    with open('./all_tables.txt', 'r') as f:
        all_tables = f.read().splitlines()
        f.close()
    with open('./imported_tb.txt', 'r') as f:
        imported_tables = f.read().splitlines()
        f.close()

    not_import = set(all_tables).difference(imported_tables)
    return not_import


def import_table(tables):
    # 由于sqoop又调用了java命令，所以使用nohup才能读取输出
    cmd = 'nohup sqoop import --connect jdbc:oracle:thin:@172.20.14.164:1521:orcl --username qzxy --password qzxy@123 --table %s --hive-import -m 1 --hive-database usr_zsj --create-hive-table --hive-overwrite &'
    for tb in tables:
        p = subprocess.Popen(cmd % tb, stdout=subprocess.PIPE,shell=True)
        res = p.stdout.readlines()
        logging.info(res)
        print 'Import result:',res[-3:]
        time.sleep(3)


if __name__ == '__main__':
    # not_import = compute_table()
    not_import = ['M_REC_CONSUME']
    print '未完成的表数：%s \n开始执行导入命令...' % len(not_import)
    import_table(not_import)
    print 'Import Completed!'
