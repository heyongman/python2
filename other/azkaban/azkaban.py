# -*- encoding:utf-8 -*-

import requests
import os
import sys
import json
import urllib3
from optparse import OptionParser
from optparse import OptionGroup

# 关闭调用api请求返回的警告
# requests.packages.urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 禁止不安全警告

# 定义azkaban地址、登录信息
str_url = 'https://104.1.67.207:8443'


# 登录azkaban
# username: 登录用户名
# password: 登录密码
def login(username, password):
    # 登录信息
    postdata = {'username': username, 'password': password}

    # 登录，通过verify=False关闭安全验证
    login_url = str_url + '?action=login'
    r = requests.post(login_url, postdata, verify=False).json()

    return r


# 创建一个项目
# projectname:指定的项目名称
# description:项目说明，不允许为空。
def create_project(sessionid, projectname, description):
    postdata = {'session.id': sessionid, 'name': projectname, 'description': description}

    upload_url = str_url + '/manager?action=create'
    r = requests.post(upload_url, postdata, verify=False).json()

    return r


# 删除项目
# projectname:需要删除的项目名称
def delete_project(sessionid, projectname):
    postdata = {'session.id': sessionid, 'project': projectname}

    upload_url = str_url + '/manager?delete=true'
    r = requests.get(upload_url, postdata, verify=False)

    return str(r.status_code)


# 上传项目zip文件
# projectname:需要上传zip包的项目名称
# filepath:项目zip文件
def upload_project_zip(sessionid, projectname, filepath):
    # 从路径中获取文件名
    filename = os.path.basename(os.path.realpath(filepath))

    files = {'file': (filename, open(filepath, 'rb'), 'application/zip')}
    postdata = {'session.id': sessionid, 'project': projectname, 'file': files, 'ajax': 'upload'}

    upload_url = str_url + '/manager?ajax=upload'
    r = requests.post(upload_url, postdata, files=files, verify=False).json()

    return r


# 获取一个项目的flow信息
# projectname:项目名称
def fetch_flows(sessionid, projectname):
    postdata = {'session.id': sessionid, 'project': projectname, 'ajax': 'fetchprojectflows'}

    fetch_url = str_url + '/manager?ajax=fetchprojectflows'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 获取一个工作流的jobs
# projectname:项目名称
# flowid:flow名称
def fetch_jobs(sessionid, projectname, flowid):
    postdata = {'session.id': sessionid, 'project': projectname, 'ajax': 'fetchflowgraph', 'flow': flowid}

    fetch_url = str_url + '/manager?ajax=fetchflowgraph'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 获取工作流执行总体信息
# projectname:项目名称
# flowid:flow名称
# start:从最后第几次运行结果开始查
# length:查询几次的运行结果
def fetch_executions(sessionid, projectname, flowid, start, length):
    postdata = {'session.id': sessionid, 'project': projectname, 'ajax': 'fetchFlowExecutions', 'flow': flowid,
                'start': start, 'length': length}

    fetch_url = str_url + '/manager?ajax=fetchFlowExecutions'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 获取一个正在执行的工作流的情况
# projectname:项目名称
# flowid:flow名称
def fetch_running_executions(sessionid, projectname, flowid):
    postdata = {'session.id': sessionid, 'project': projectname, 'ajax': 'getRunning', 'flow': flowid}

    fetch_url = str_url + '/executor?ajax=getRunning'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 根据指定的Execution Id，获取工作流执行的详细信息
# execid:Execution Id
def fetch_flow_execution_byid(sessionid, execid):
    postdata = {'session.id': sessionid, 'ajax': 'fetchexecflow', 'execid': execid}

    fetch_url = str_url + '/executor?ajax=fetchexecflow'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 根据指定的session.id、jobid、exec_id，获取对应的任务日志
# offset:日志的偏移量，返回的日志将从第10个字符开始
# length:日志数据的长度
def fetch_execution_job_logs(sessionid, execid, jobid, offset, length):
    postdata = {'session.id': sessionid, 'ajax': 'fetchExecJobLogs', 'execid': execid, 'jobId': jobid, 'offset': offset,
                'length': length}

    fetch_url = str_url + '/executor?ajax=fetchExecJobLogs'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 获取工作流执行的更新情况
# lastUpdateTime:按上次更新时间筛选的条件。如果需要所有作业信息，则将值设置为-1。
def fetch_flow_execution_updates(sessionid, execid, lastupdatetime):
    postdata = {'session.id': sessionid, 'ajax': 'fetchexecflowupdate', 'execid': execid,
                'lastUpdateTime': lastupdatetime}

    fetch_url = str_url + '/executor?ajax=fetchexecflowupdate'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 执行一个工作流
# projectname:项目名称
# flowid:flow名称
# settings:可选参数字典
#   disabled(可选):此次执行禁用的作业名称列表。格式化为JSON数组字符串。如：["job_name_1","job_name_2","job_name_N"]
#   successEmails(可选):执行成功发送的邮件列表。多个邮箱用[,|;|\s+]分隔。如：zh@163.com,zh@126.com
#   failureEmails(可选):执行成功发送的邮件列表。多个邮箱用[,|;|\s+]分隔。如：zh@163.com,zh@126.com
#   successEmailsOverride(可选):是否使用系统默认电子邮件设置覆盖成功邮件。值：true, false
#   failureEmailsOverride(可选):是否使用系统默认电子邮件设置覆盖失败邮件。值：true, false
#   notifyFailureFirst(可选):是否在第一次失败时发送电子邮件通知。值：true, false
#   notifyFailureLast(可选):是否在最后失败时发送电子邮件通知。值：true, false
#   failureAction(可选):如果发生错误，如何操作。值：finishcurrent、cancelimmediately、finishpossible
#   concurrentOption(可选):如果不需要任何详细信息，请使用ignore。值：ignore, pipeline, skip
#   flowOverride[flowProperty](可选):用指定的值重写指定的流属性。如：flowoverride[failure.email]=abc@163.com
def execute_flow(sessionid, projectname, flowid, settings):
    postdata = {'session.id': sessionid, 'ajax': 'executeFlow', 'project': projectname, 'flow': flowid}
    for key in settings:
        postdata[key] = settings[key]

    fetch_url = str_url + '/executor?ajax=executeFlow'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 取消一个正在运行的工作流
# execid:Execution id
def cancel_flow_execution(sessionid, execid):
    postdata = {'session.id': sessionid, 'ajax': 'cancelFlow', 'execid': execid}

    fetch_url = str_url + '/executor?ajax=cancelFlow'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 暂停一个正在运行的工作流
# execid:Execution id
def pause_flow_execution(sessionid, execid):
    postdata = {'session.id': sessionid, 'ajax': 'pauseFlow', 'execid': execid}

    fetch_url = str_url + '/executor?ajax=pauseFlow'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 恢复一个已暂停的工作流
# execid:Execution id
def resume_flow_execution(sessionid, execid):
    postdata = {'session.id': sessionid, 'ajax': 'resumeFlow', 'execid': execid}

    fetch_url = str_url + '/executor?ajax=resumeFlow'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 使用cron灵活设置调度
# projectname:项目名称
# flowid:flow名称
# cronExpression:cron表达式。如："0 23/30 5,7-10 ? * 6#3"
def flexible_scheduling_using_cron(sessionid, projectname, flowid, cronexpression):
    postdata = {'session.id': sessionid, 'ajax': 'resumeFlow', 'projectName': projectname, 'flow': flowid,
                'cronExpression': cronexpression}

    fetch_url = str_url + '/schedule?ajax=scheduleCronFlow'
    r = requests.post(fetch_url, postdata, verify=False).json()

    return r


# 获取指定Project、flow的调度
# projectid:项目id
# flowid:flow名称
def fetch_schedule(sessionid, projectid, flowid):
    postdata = {'session.id': sessionid, 'projectId': projectid, 'ajax': 'fetchSchedule', 'flowId': flowid}

    fetch_url = str_url + '/schedule?ajax=fetchSchedule'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


# 取消工作流的调度
# scheduleId:计划的ID。可以在scheduling页面找到
def unschedule_flow(sessionid, scheduleid):
    postdata = {'session.id': sessionid, 'scheduleId': scheduleid}

    fetch_url = str_url + '/schedule?action=removeSched'
    r = requests.post(fetch_url, postdata, verify=False).json()

    return r


# 设置告警模块
# scheduleId:计划的ID
# slaEmails:SLA警报电子邮件列表。如：zh@163.com;zh@126.com
# settings:SLA规则字典。格式为settings[…]=[id],[rule],[durati on],[emailAction],[killAction]。
#       如：{"settings[0]":"aaa,SUCCESS,5:00,true,false";"settings[1]":"bbb,SUCCESS,10:00,false,true"}
def set_sla(sessionid, scheduleid, slaemails, settings):
    postdata = {'session.id': sessionid, 'ajax': 'setSla', 'scheduleId': scheduleid, 'slaEmails': slaemails}
    for key in settings:
        postdata[key] = settings[key]

    fetch_url = str_url + '/schedule?ajax=setSla'
    r = requests.post(fetch_url, postdata, verify=False).json()

    return r


# 获取资源调度的报警模块
# scheduleId:计划的ID
def fetch_sla(sessionid, scheduleid):
    postdata = {'session.id': sessionid, 'ajax': 'slaInfo', 'scheduleId': scheduleid}

    fetch_url = str_url + '/schedule?ajax=slaInfo'
    r = requests.get(fetch_url, postdata, verify=False).json()

    return r


def execute(url):
    parser = get_option_parser()
    options, args = parser.parse_args(sys.argv[1:])
    print options, args
    if options.postParam:
        url = url + 'register'
        with open(options.postParam, 'r') as f:
            for line in f:
                json_line = json.loads(line, encoding='utf-8')
                # res, stat = HttpMethod.post(url=url, params=json_line)
                # print res, stat
    elif options.resumeParam:
        pass
    elif options.pauseParam:
        pass
    elif options.startParam:
        pass
    elif options.startParam:
        pass
    else:
        print 'Options cannot be recognized, try type -h to get help.'


def get_option_parser():
    usage = "usage: %prog options [config-path]"
    parser = OptionParser(usage=usage)

    option_group = OptionGroup(parser, "Program Options")
    option_group.add_option("-c", metavar="<create connector using config file>", dest="postParam", action="store",
                            help="JSON inline format config ")
    option_group.add_option("-r", metavar="<resume a paused connector>", dest="resumeParam", action="store",
                            help="* means resume all connector")
    option_group.add_option("-p", metavar="<pause a paused connector>", dest="pauseParam", action="store",
                            help="* means pause all connector")
    option_group.add_option("-s", metavar="<start worker>", dest="startParam", action="store_true", help="start worker")
    option_group.add_option("-k", metavar="<pause all connector and stop worker>", dest="killParam",
                            action="store_true", help="pause all connector and stop worker")
    parser.add_option_group(option_group)
    return parser


if __name__ == '__main__':
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    # execute('')
    res = login('azkaban', 'azkaban')
    session_id = res.get('session.id')
    # res = create_project(session_id, 'dwd', 'dwd层调度项目')
    res = upload_project_zip(session_id, 'dwd', 'path')
    res.get()

