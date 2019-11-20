#!/usr/bin/env python
# coding=utf-8
import json
import logging.config
import os
import re
import subprocess
import sys
import time
import math
from datetime import date, timedelta, datetime
from fnmatch import fnmatch

# import global_variable as gv
import http_method


# log config
curr_path = os.path.dirname(os.path.abspath(__file__))
log_path = curr_path + os.sep + 'merge_scheduler.log'
log_config = {'version': 1, 'formatters': {'simple': {'format': '%(asctime)s - %(levelname)s - %(message)s'}},
              'handlers': {'console': {'class': 'logging.StreamHandler', 'level': 'INFO', 'formatter': 'simple'},
                           'file': {'class': 'logging.FileHandler', 'filename': 'merge_scheduler_error.log',
                                    'level': 'ERROR', 'formatter': 'simple'},
                           'rotaFile': {'class': 'logging.handlers.TimedRotatingFileHandler',
                                        'filename': 'merge_scheduler.log', 'level': 'DEBUG', 'formatter': 'simple',
                                        'when': 'd', 'interval': 1, 'backupCount': 10}, },
              'loggers': {'ConsoleFileLogger': {'handlers': ['console', 'file', 'rotaFile'], 'level': 'DEBUG'}}}

logging.config.dictConfig(log_config)
log = logging.getLogger("ConsoleFileLogger")


class Job:

    def __init__(self):
        try:
            conf_path = sys.argv[1]
            with open(conf_path, 'r') as f:
                conf = json.load(f)
            log.info("Job config:\n%s", conf)
        except Exception as e:
            log.error('Read job config error: %s\n\n', e)
            sys.exit(1)
        self.get_size_tmpt = "source /etc/profile\nhdfs dfs -du -s %s | awk 'BEGIN{SUM=0}{SUM += $1}END{print SUM}'"
        self.replica_ids = conf.get('replica_ids')
        self.exclude_table = conf.get('exclude_table')
        # eg: zg_zd.vio_log, support for wildcard matching
        self.using_table = conf.get('using_table')
        self.before_days = conf.get('before_days')
        # self.schema_map = {'R_ZG_ZD2': 'zg_zd', 'R_ND_ZW2': 'nd_zw'}
        self.schema_map = conf.get('schema_map')
        self.app_ids_path = conf.get('app_ids_path')
        self.table_prefix = conf.get('table_prefix')
        self.table_suffix = conf.get('table_suffix')
        self.replica_id = ''
        self.hdfs_base_url = ''
        self.curr_ymd = ''
        self.is_first_loop = True
        self.is_check_status = conf.get('is_check_status')
        self.jar_path = conf.get('jar_path')
        self.cmd_tmpt = '''
                        spark-submit --class com.core.merge.Test \\\
                        --master yarn \\\
                        --deploy-mode cluster \\\
                        --driver-memory %s \\\
                        --executor-memory %s \\\
                        --executor-cores %s \\\
                        --num-executors %s \\\
                        --name merge_scheduler \\\
                        --queue merge_scheduler \\\
                        --conf spark.driver.maxResultSize=0 \\\
                        %s "%s" "%s"
                        '''

    def start(self):
        # restore:('R_ZG_ZD2',-2,'2019-09-30',['table_name']
        restore_replica, restore_ymd, restore_before_days, restore_tasks = self.restore()
        if restore_replica is not None:
            log.info('Restore from last status, replica: %s, day: %s, before days: %s, failed task num: %s',
                     restore_replica, restore_ymd, restore_before_days, len(restore_tasks))
            self.before_days = restore_before_days

        # replica loop
        for replica in self.replica_ids:
            self.replica_id = replica
            self.hdfs_base_url = '/ogg/%s/' % replica
            if self.is_first_loop and restore_replica in self.replica_ids and not replica == restore_replica:
                log.info('Current replica %s skipped based on checkpoint file.', replica)
                continue

            # day loop
            for day in range(self.before_days, 0):
                self.curr_ymd = (date.today() + timedelta(days=day)).strftime('%Y-%m-%d')
                log.info('Current merge replica: %s, day: %s, using tables: %s, exclude table: %s', replica,
                         self.curr_ymd, self.using_table, self.exclude_table)

                # get increased tables
                inc_table = self.get_inc_table()  # set((zg_zd.hive_vio_log,TRFF_APP.VIO_LOG))
                if self.is_first_loop:
                    # self.is_first_loop = False
                    if restore_replica:
                        # filter out the last unsuccessful task
                        filtered_table = filter(lambda (tb, ori_tb): tb in restore_tasks, inc_table)
                        log.info('%s tasks skipped based on checkpoint, %s tasks will be submitted.', len(inc_table) - len(filtered_table), len(filtered_table))
                        inc_table = filtered_table
                    else:
                        log.info('%s tasks skipped based on checkpoint, %s tasks will be submitted.', 0, len(inc_table))

                # build task
                task_config_list = self.build_task(inc_table)
                # log.debug('Task count: %s, configs: %s', len(task_config_list), task_config_list)
                log.info('Task count: %s, sample configs: %s', len(task_config_list), task_config_list[:2])

                index = 1
                for config in task_config_list:
                    # compute driver memory
                    self.compute_config_size(config)
                    # replace \ to \n for print
                    log_shell = self.cmd_tmpt.replace('\\', '\n') % (
                        config['driver_memory'], config['executor_memory'], config['executor_cores'],
                        config['num_executors'], self.jar_path, config['hdfs_path'], config['table'])
                    log.info('Prepare to submit job(%s/%s),submit command:%s', index, len(task_config_list), log_shell)
                    index += 1

                    # submit task
                    # app_id = self.submit(config)
                    app_id = 'application_1563269271647_23029'

                    # Save job status and failed jobs.
                    config['app_id'] = app_id
                    self.save_status(task_config_list)

                    # copy for web server
                    # gv.set_value(task_config_list)
                    time.sleep(1)

                # after current day merge job submitted,check status
                log.info('Start check current job status.')
                status = self.check_status()
                if not status:
                    log.error('System exit!')
                    sys.exit(1)

    def check_status(self):
        if self.is_first_loop:
            self.is_first_loop = False
            if not self.is_check_status:
                log.info('Ignore first status check.\n\n')
                return True
        try:
            with open(self.app_ids_path, 'r') as f:
                task_config_list = json.load(f)
            if task_config_list is None:
                return True
            # get -1 day all yarn job status
            id_status = http_method.get_app_status(-1)
            # set merge job status
            running_jobs = []
            not_succeed_jobs = []
            for config in task_config_list:
                status = id_status.get(config.get('app_id'))
                config['status'] = status
                if status == 'UNDEFINED':
                    running_jobs.append(config['table'])
                elif not status == 'SUCCEEDED':
                    not_succeed_jobs.append(config['table'])
            if len(running_jobs) > 0:
                log.info('Waiting for %s running job: %s', len(running_jobs), running_jobs)
                time.sleep(60)
                return self.check_status()
            elif len(not_succeed_jobs) > 0:
                log.error('Job contains %s not succeed tasks,please check and restore! Detail: %s\n\n', len(not_succeed_jobs), not_succeed_jobs)
                return False
            else:
                log.info('Check status info: Succeeded, replica: %s, day: %s.\n\n', self.replica_id, self.curr_ymd)
                return True
        except IOError as e:
            log.info('Check status info: %s.\n\n', e)
            return True
        except Exception as e:
            log.error('Check status error: %s.\n\n', e)
            return False

    def save_status(self, task_config_list):
        try:
            dump = json.dumps(task_config_list)
            app_ids_dir = os.path.dirname(os.path.abspath(self.app_ids_path))
            if not os.path.isdir(app_ids_dir):
                os.makedirs(app_ids_dir)
            with open(self.app_ids_path, 'w') as f:
                f.write(dump)
            log.info('Task status saved.')
        except Exception as e:
            log.error('Failed to save task status: %s', e)
            sys.exit(1)

    def submit(self, config):
        # replace \ to blank for submit
        shell = self.cmd_tmpt.replace('\\', '') % (
            config['driver_memory'], config['executor_memory'], config['executor_cores'],
            config['num_executors'], self.jar_path, config['hdfs_path'], config['table'])
        try:
            p = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while p.poll() is None:
                with p.stdout:
                    for line in iter(p.stdout.readline, b''):
                        line = line.rstrip()
                        log.debug(line)
                        if 'Submitted application' in line:
                            mat = re.match(r'.*Submitted application (.*)', line)
                            if mat:
                                app_id = mat.group(1)
                                log.info('Application submitted successfully.\n')
                                return app_id
                            else:
                                log.error('Application id not found!\n')
                        elif 'Exception in' in line:
                            log.error('Application submitted failed! submit command:%s\nCause:\n%s', shell, line)
        except Exception as e:
            log.error('Job submit failed:\n%s\n', e)

    def compute_config_size(self, config):
        shell = self.get_size_tmpt % config['hdfs_path']
        log.debug('Start calculating memory size,command:%s', shell)
        p = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ret = p.wait()
        if ret == 0:
            inc_size = int(p.stdout.read().strip()) / 1024.0 / 1024 / 1024  # GB
            config['inc_size'] = round(inc_size * 1024, 3)
            log.info('Current inc size: %.3f MB, hdfs path: %s', inc_size * 1024, config['hdfs_path'])
            config['driver_memory'] = str(int(math.ceil(1 + inc_size * 15))) + 'G'
            config['executor_memory'] = str(int(math.ceil(1 + inc_size * 5))) + 'G'
            config['executor_cores'] = str(int(round(1 + (inc_size - 0.001) * 4)))
            config['num_executors'] = str(int(math.ceil(1 + (inc_size - 0.001) * 15)))
        else:
            log.error('Get inc size error,command: %s\nWill use 1G as the default.', shell)
            return '1G'
        pass

    def build_task(self, inc_table):
        task_config_list = []
        for lower_table, ori_table in inc_table:
            task_config_list.append(
                {'table': lower_table, 'hdfs_path': self.hdfs_base_url + self.curr_ymd + '_*/' + ori_table + '-*'})
        return task_config_list

    def get_inc_table(self):
        # inc_table: set((zg_zd.hive_vio_log,TRFF_APP.VIO_LOG))
        inc_table = set()
        exclude_tables = set()
        # 12 hour
        for i in range(1, 13):
            # /ogg/R_ZG_ZD2/2019-08-29_00
            hdfs_path = self.hdfs_base_url + self.curr_ymd + '_' + str(i).zfill(2)
            log.debug('Get inc size path: %s', hdfs_path)
            file_statuses = http_method.get_hdfs_info(hdfs_path)
            for file_status in file_statuses:
                origin_table = file_status.get('pathSuffix')[:-24]
                head, sep, tail = origin_table.encode('utf-8').partition('.')
                schema = self.schema_map.get(self.replica_id)
                if not schema:
                    log.error('Can not find schema mapping with: %s ,current table: %s will be ignored!', self.replica_id,
                              origin_table)
                    continue
                hive_table = (schema + '.' + self.table_prefix + tail + self.table_suffix).lower()
                exclude_flag = False
                # exclude table
                for exclude_table_mat in self.exclude_table:
                    if fnmatch(hive_table, exclude_table_mat):
                        exclude_flag = True
                        exclude_tables.add(hive_table)
                        break
                if exclude_flag:
                    continue
                # add table
                for using_table_mat in self.using_table:
                    if fnmatch(hive_table, using_table_mat):
                        inc_table.add((hive_table, origin_table))
        log.info('Got %s increased table, %s will be excluded: %s', len(inc_table), len(exclude_tables), exclude_tables)
        return inc_table

    def restore(self):
        # restore by app_ids file, return not succeeded tasks
        restore_tasks = []
        try:
            with open(self.app_ids_path, 'r') as f:
                app_infos = json.load(f)
            if len(app_infos) < 1:
                log.info('Application ids file not found, restore skipped.')
                return None, None, None, restore_tasks
            # restore last replica and date
            hdfs_path_splits = app_infos[0]['hdfs_path'].split('/')
            restore_ymd = hdfs_path_splits[-2][:-2]
            restore_before_days = -(datetime.today() - datetime.strptime(restore_ymd, '%Y-%m-%d')).days
            restore_replica = hdfs_path_splits[-3]
            # get succeeded task
            id_status = http_method.get_app_status(restore_before_days)
            if len(id_status) < 1:
                return None, None, None, restore_tasks
            for app_info in app_infos:
                app_id = app_info.get('app_id')
                if not id_status.get(app_id) == 'SUCCEEDED':
                    restore_tasks.append(app_info['table'])
            # log.info('Restore from last job,succeeded task num: %s', len(restore_tasks))
            return restore_replica, restore_ymd, restore_before_days, restore_tasks
        except Exception as e:
            log.warn('Restore failed: %s', e)
            return None, None, None, restore_tasks


if __name__ == '__main__':
    # port = 9999
    # res = http_method.port_detection('127.0.0.1', port)
    # if res:
    #     log.error('Port %s is already in use.', port)
    #     sys.exit(1)
    # gv.init()
    # threading.Thread(target=web_controller.start, args=(port,)).start()
    # log.info('Web server started,current port:%s.', port)
    Job().start()
    log.info('Merge job started.')
