#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import datetime
import json
import os
import configparser
import time

from easemob.emclient import *
from utils.DB import DB
from utils.extract import extract
from utils.ungz import un_gz

# 读取配置文件
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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


def do_it(message_time):
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
                data['payload'] = json.dumps(data['payload'],ensure_ascii=False)
                data['created_at'] = data['updated_at'] = now
                # list.append(list(data.values()))
                p = [data['msg_id'], data['timestamp'], data['direction'], data['to'], data['from'], data['chat_type'],
                     data['payload'],data['created_at'], data['updated_at']]
                newData.append(p)
                print(newData)
            # 入库
            db = DB(config)
            db.insert(newData)
    else:
        print('请求错误:状态码' + str(response.code))
    return response.code


if __name__ == '__main__':
    client = PyClient(APP_KEY, DEFAULT_REST, CLIENT_ID, CLIENT_SECRET)
    # 获取token
    print('###任务开始执行')
    nowTimestamp = int(time.time())
    if len(TOKEN) == 0 or nowTimestamp - LAST_GET_TIME > 86400:
        print('####管理员token已过期，获取中……')
        client.get_admin_token(CLIENT_ID, CLIENT_SECRET)
        config.set('huanxin', 'token', client.admin_token)
        config.set('huanxin', 'last_get_time', str(nowTimestamp))
        config.write(open(configFile, "w"))
    else:
        client.admin_token = TOKEN
    print('####管理员token：' + client.admin_token)
    client.admin_rest_token = 'Bearer ' + client.admin_token

    if nowTimestamp - LAST_MESSAGE_TIME > 7200:
        print('####开始执行未完成的任务')
    while nowTimestamp - LAST_MESSAGE_TIME >= 7200:
        timeArray = time.localtime(LAST_MESSAGE_TIME)
        q = time.strftime("%Y%m%d%H", timeArray)
        print('####获取' + q + "的聊天记录")
        result = do_it(q)
        if result == 0 or result == 404:
            LAST_MESSAGE_TIME += 3600
            config.set('huanxin', 'last_message_time', str(LAST_MESSAGE_TIME))
            config.write(open(configFile, "w"))
        if nowTimestamp - LAST_MESSAGE_TIME > 3600:
            print('####休息1分钟')
            time.sleep(50)
    print('#####任务完成')
