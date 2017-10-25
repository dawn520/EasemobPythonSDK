#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import datetime
import json
import os
import configparser
import socket
import time

import sys

import logging

from easemob.emclient import *
from utils.DB import DB
from utils.extract import extract
from utils.ungz import un_gz

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 开启日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logfile = os.path.join(BASE_DIR, "log/log.txt")
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
# 进程锁，同时只能执行一个脚本
try:
    hyf_suo = socket.socket()
    add = ('', 24961)
    hyf_suo.bind(add)
except Exception as e:
    print(e)
    logger.info('already has an instance')
    sys.exit()
# 读取配置文件
config = configparser.ConfigParser()
configFile = os.path.join(BASE_DIR, "config.conf")
config.read(configFile)
APP_KEY = config.get('huanxin', 'app_key')
CLIENT_ID = config.get('huanxin', 'client_id')
CLIENT_SECRET = config.get('huanxin', 'client_secret')
DEFAULT_REST = config.get('huanxin', 'default_rest')
TOKEN = config.get('huanxin', 'token')
LAST_GET_TIME = int(config.get('huanxin', 'last_get_time'))
LAST_MESSAGE_TIME = int(config.get('huanxin', 'last_message_time'))


def do_it(client, message_time):
    filename = 'temp/' + message_time + '.gz'
    response = client.get_history_message(message_time)
    if response.code == 0:
        # 获取下载文件URL
        url = response.data['data'][0]['url']
        # 获取目录
        filename = os.path.join(BASE_DIR, filename)
        if client.download_file(url, filename):
            jsonStr = un_gz(filename)
            newData = []
            now = datetime.datetime.now()
            for line in jsonStr:
                line = str(line, encoding='utf-8')
                data = json.loads(line, encoding='utf-8')
                # print(data)
                data['payload'] = json.dumps(data['payload'], ensure_ascii=False)
                data['created_at'] = data['updated_at'] = now
                # list.append(list(data.values()))
                p = [data['msg_id'], data['timestamp'], data['direction'], data['to'], data['from'], data['chat_type'],
                     data['payload'], data['created_at'], data['updated_at']]
                newData.append(p)
                print(newData)
            # 入库
            db = DB(config)
            db.insert(newData)
    else:
        logger.info('请求错误:状态码' + str(response.code))
    return response.code

if __name__ == '__main__':
    try:
        client = PyClient(APP_KEY, DEFAULT_REST, CLIENT_ID, CLIENT_SECRET)
        # 获取token
        logger.info('任务开始执行')
        nowTimestamp = int(time.time())
        if len(TOKEN) == 0 or nowTimestamp - LAST_GET_TIME > 86400:
            logger.info('管理员token已过期，获取中……')
            code = client.get_admin_token(CLIENT_ID, CLIENT_SECRET)
            while code != 1:
                logger.info('获取失败，,状态码：' + str(code) + ',休息一分钟再获取')
                time.sleep(60)
            config.set('huanxin', 'token', client.admin_token)
            config.set('huanxin', 'last_get_time', str(nowTimestamp))
            config.write(open(configFile, "w"))
        else:
            client.admin_token = TOKEN
        logger.info('管理员token：' + client.admin_token)
        client.admin_rest_token = 'Bearer ' + client.admin_token

        if nowTimestamp - LAST_MESSAGE_TIME > 3600*24*3:
            logger.info('设置获取聊天记录的时间大于三天，程序已自动设置为三天前')
            LAST_MESSAGE_TIME = nowTimestamp - 3600*24*3
        if nowTimestamp - LAST_MESSAGE_TIME > 7200:
            logger.info('开始执行未完成的任务')
        while nowTimestamp - LAST_MESSAGE_TIME >= 7200:
            timeArray = time.localtime(LAST_MESSAGE_TIME)
            q = time.strftime("%Y%m%d%H", timeArray)
            logger.info('获取' + q + "的聊天记录")
            result = do_it(client, q)
            if result == 0 or result == 404:
                LAST_MESSAGE_TIME += 3600
                config.set('huanxin', 'last_message_time', str(LAST_MESSAGE_TIME))
                config.write(open(configFile, "w"))
            if nowTimestamp - LAST_MESSAGE_TIME > 3600:
                logger.info('休息1分钟')
                time.sleep(60)
        logger.info('任务完成')
        sys.exit()
    except KeyboardInterrupt:
        logger.info('你已经退出程序')
        sys.exit()

