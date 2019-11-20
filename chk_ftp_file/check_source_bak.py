# coding=utf-8
import os
import logging
import shutil
import time
import hashlib

curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(curr_path, "check_source.log")
src_data_prefix = "zd"  # 源数据文件前缀
src_data_dir = os.path.join(curr_path, "src")  # 源端数据目录
dst_data_dir = os.path.join(curr_path, "dst")  # 目标端数据目录
first_file_path = os.path.join(src_data_dir, src_data_prefix + "000000")  # 源端0号文件的全路径
status_file = os.path.join(curr_path, ".status")
max_no = 999999

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=log_path, level=logging.DEBUG, format=LOG_FORMAT)
# log = logging.getLogger()
# log.addHandler(logging.StreamHandler())  # 控制台打印


class Check:

    def __init__(self):
        self.is_first = True
        self.self_inc_id = 0  # 自增主键的初始值
        self.file_index = 0  # 根据当前编号的源文件index
        self.last_zero_time = ""  # 上一次0号文件的日期
        self.last_time = ""  # 上一次传输文件的日期
        self.last_md5 = ""  # 上一次传输文件的md5

    def first_check(self):
        if self.is_first:
            try:
                with open(status_file, "r") as f:
                    self.self_inc_id = int(f.readline().strip())
                    self.file_index = int(f.readline().strip())
                    self.last_zero_time = f.readline().strip()
                    self.last_time = f.readline().strip()
                    self.last_md5 = f.readline().strip()
            except Exception as e:
                logging.error(e)

            # 保存0号文件的创建日期
            if self.file_index == 0 and os.path.exists(first_file_path):
                self.last_zero_time = str(os.path.getctime(first_file_path))

            logging.info(
                "获取到上次状态: self_inc_id: %s | file_index: %s | last_zero_time: %s | last_time: %s | last_md5 : %s",
                self.self_inc_id, self.file_index, self.last_zero_time, self.last_time, self.last_md5)

            self.is_first = False

    def check_file(self):
        self.first_check()

        while True:
            src_data_path = os.path.join(src_data_dir, src_data_prefix + str(self.file_index).zfill(6))
            next_src_data_path = os.path.join(src_data_dir, src_data_prefix + str(self.file_index + 1).zfill(6))
            logging.info("新的状态: self_inc_id: %s | file_index: %s | last_zero_time: %s | last_time: %s | last_md5 : %s",
                         self.self_inc_id, self.file_index, self.last_zero_time, self.last_time, self.last_md5)

            # logging.info("src_data_path：%s | next_src_data_path：%s", src_data_path, next_src_data_path)
            if os.path.exists(src_data_path) and os.path.exists(next_src_data_path):
                # 如果下一个文件已经生成就将上一个文件复制过去
                # logging.info("当前处理文件：%s", src_data_path)

                # 将源文件拷贝到目标目录下
                if not os.path.exists(dst_data_dir):
                    logging.info("目标目录不存在，即将创建：%s", dst_data_dir)
                    os.makedirs(dst_data_dir)
                dst_path = os.path.join(dst_data_dir, src_data_prefix + str(self.self_inc_id).zfill(6))
                shutil.copy(src_data_path, dst_path)
                logging.info("将 %s 复制到 %s 完成", src_data_path, dst_path)

                # 获取新的状态
                self.last_time = str(os.path.getctime(src_data_path))
                self.last_md5 = cert_util(src_data_path)
                if self.file_index == 0:
                    self.last_zero_time = os.path.getctime(first_file_path)

                # copy完成，状态数+1
                self.self_inc_id += 1
                self.file_index += 1

                # 如果编号达到了最大值就重置为0
                if self.file_index > max_no:
                    self.file_index = 0
                    self.self_inc_id = 0

                # 将状态保存到文件
                with open(status_file, "w") as f:
                    f.write(str(self.self_inc_id) + "\n")
                    f.write(str(self.file_index) + "\n")
                    f.write(str(self.last_zero_time) + "\n")
                    f.write(str(self.last_time) + "\n")
                    f.write(str(self.last_md5) + "\n")

                logging.info(
                    "保存处理后的状态: self_inc_id: %s | file_index: %s | last_zero_time: %s | last_time: %s | last_md5 : %s",
                    self.self_inc_id, self.file_index, self.last_zero_time, self.last_time, self.last_md5)

            else:
                # 否则等待0.5秒
                time.sleep(3)

                # 判断当前0号文件与上次记录的0号文件创建时间是否相同
                # 不相同就重新搜索新的文件index
                if os.path.exists(first_file_path) and self.last_zero_time != str(os.path.getctime(first_file_path)):
                    src_filenames = os.listdir(src_data_dir)
                    for i in range(0, len(src_filenames) + 1):  # 多加一位，保险
                        f = os.path.join(src_data_dir, src_data_prefix + str(i).zfill(6))
                        while True:
                            if os.path.exists(f):
                                logging.info("当前查找的文件： %s | getctime：%s | last_time", f, os.path.getctime(f), self.last_time)
                                break
                            else:
                                time.sleep(2)

                        # 寻找新的开始编号
                        # 当前遍历到的文件创建时间、md5与上次的一样
                        # 就把当前文件index+1赋值给file_index
                        if os.path.exists(f) and (str(os.path.getctime(f)) == self.last_time) and (self.last_md5 == cert_util(f)):
                            self.file_index = i + 1
                            self.last_zero_time = str(os.path.getctime(first_file_path))
                            logging.info("找到了新的处理编号: %s\n", self.file_index)
                            break


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


if __name__ == '__main__':
    Check().check_file()
