# coding=utf-8

"""
1. log
some operation with log
"""
import logging
import os
import json

# 1. create log collector
import time

import paramiko

log = logging.getLogger(name="rose_logger")
# 2. create different log output channel
# output to console
pycharm = logging.StreamHandler()
# output to file
file = logging.FileHandler(os.getcwd() + r"\rule.log", encoding="utf-8")
# 3. create output log format
fmt1 = "%(asctime)s - [%(funcName)s-->line:%(lineno)d] - %(levelname)s:%(message)s"
# create a log output object
pycharm_fmt1 = logging.Formatter(fmt=fmt1)
# 4. use log format to combine log object
pycharm.setFormatter(fmt=pycharm_fmt1)
file.setFormatter(fmt=pycharm_fmt1)
# 5. set log level
log.setLevel(level=logging.DEBUG)
# 6. output log to different channel
log.addHandler(pycharm)
log.addHandler(file)


# encoding: utf-8
import os
import yaml
import sys


def read_configuration_file(filename_path):
    """
    解析json配置文件，读取相关配置项
    :return:
    """
    try:
        with open(filename_path, 'r', encoding="utf-8") as conf_file:
            conf_data = conf_file.read()
            conf_dict = yaml.full_load(conf_data)
        linux = conf_dict.get('linux')
        mysql = conf_dict.get('mysql')
        k8s = conf_dict.get('k8s')
        return (
            linux,
            mysql,
            k8s,
        )
    except Exception as e:
        log.exception(msg=e)


# DAC配置项的json文件路径
BASE_DIR = None
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
elif __file__:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(BASE_DIR, "configuration.yaml")

# 读取json文件，获取所有配置项的信息
(
    linux,
    mysql,
    k8s,
) = read_configuration_file(json_path)

# TSDB  config
LINUX_HOST = linux["host"]
LINUX_PORT = linux["port"]
LINUX_USER = linux["username"]
LINUX_PASSWORD = linux["password"]

# mysql config
MYSQL_HOST = mysql['host']
MYSQL_PORT = mysql['port']
MYSQL_DATABASE = mysql['database']
MYSQL_USERNAME = mysql['username']
MYSQL_PASSWORD = mysql['password']


K8S_COMMAND = k8s['command']

import pymysql


def execute_sql(sql):
    connect = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USERNAME, passwd=MYSQL_PASSWORD,
                              db=MYSQL_DATABASE, port=int(MYSQL_PORT), charset="utf8")
    cursor = connect.cursor()
    cursor.execute(sql)
    cursor.close()
    # 删除操作要commit
    connect.commit()
    connect.close()


def get_execute_sql(sql):
    connect = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USERNAME, passwd=MYSQL_PASSWORD,
                              db=MYSQL_DATABASE, port=int(MYSQL_PORT), charset="utf8")
    cursor = connect.cursor()
    cursor.execute(sql)
    re1 = cursor.fetchall()
    cursor.close()
    connect.close()
    return re1


def delete_hive_db_lock(host_name):
    delete_sql = '''delete from HIVE_LOCKS where HL_HOST="{}"'''.format(host_name)
    print(delete_sql)
    execute_sql(delete_sql)


def get_all_lock():
    d1 = get_execute_sql("select HL_HOST from HIVE_LOCKS")
    d2 = [item[0] for item in d1]
    return d2


def judge_death_lock(exist_k8_host_list, hive_db_lock_host):
    # 判断并删除不在已存在的k8的host的值
    for item in hive_db_lock_host:
        if item not in exist_k8_host_list:
            print(item)
            delete_hive_db_lock(item)


def login_linux(op, hostname, username, password):
    try:
        # 创建ssh对象
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=hostname, port=22, username=username, password=password)
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(op)

        # 获取命令结果
        result = stdout.read()
        # 将types转为str
        result = result.decode('UTF-8').replace('\n', '')
        ssh.close()
        return result
    except Exception as e:
        print(e)
    finally:
        ssh.close()


def split_json(format_dict):
    split_re = []
    if not format_dict:
        return split_re
    for item in format_dict['items']:
        split_re.append(item['metadata']['name'])
    return split_re


if __name__ == '__main__':
    while 1:
        token_ = login_linux('kubectl -n kube-system describe $(kubectl -n kube-system get secret -n kube-system -o name | grep namespace) | grep token', LINUX_HOST, LINUX_USER, LINUX_PASSWORD)
        index = token_.rfind(' ')
        format_re = token_[index + 1:]
        get_host_name_command = 'curl -H "Authorization: Bearer ' + format_re + '" ' + K8S_COMMAND + ' --insecure'
        print(get_host_name_command)
        re = login_linux(get_host_name_command, LINUX_HOST, LINUX_USER, LINUX_PASSWORD)
        print(re)
        exist_healthy_host = split_json(json.loads(re))
        lock_host = get_all_lock()
        judge_death_lock(exist_healthy_host, lock_host)
        print(exist_healthy_host)
        print(lock_host)
        time.sleep(60)


