#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import json
import os
import configparser

from easemob.emclient import *
from utils.extract import extract
from utils.ungz import un_gz

# 读取配置文件
config = configparser.ConfigParser()
config.read("./config.conf")
APP_KEY = config.get('huanxin', 'APP_KEY')
CLIENT_ID = config.get('huanxin', 'CLIENT_ID')
CLIENT_SECRET = config.get('huanxin', 'CLIENT_SECRET')
DEFAULT_REST = config.get('huanxin', 'DEFAULT_REST')
print(APP_KEY)

if __name__ == '__main__':
    client = PyClient(APP_KEY, DEFAULT_REST, CLIENT_ID, CLIENT_SECRET)
    # 获取管理员权限
    # client.get_admin_token(CLIENT_ID, CLIENT_SECRET)
    # client.admin_token = 'YWMtcOH2aIudEeeFsKVkFP7ffQAAAAAAAAAAAAAAAAAAAAG6RN8wINgR57kbyf0xVXH2AgMAAAFeJssYLw' \
    #                      'BPGgCsdoOrr0JUclzqqwuBzb7qTHNpDgdBcLzkTLnzefhPDg'
    # # print (client.admin_token)
    # time = '2017082816'
    # filename = 'temp/'+time + '.gz'
    # response = client.get_history_message(time)
    # if response.code == 0:
    #     # 获取下载文件URL
    #     url = response.data['data'][0]['url']
    #     # 获取目录
    #     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #     filename = os.path.join(BASE_DIR, filename)
    #     if client.download_file(url, filename):
    #         jsonStr = un_gz(filename)
    #         # data = json.loads(jsonStr)
    #         # print(data)
    # else:
    #     print('请求错误:状态码'+str(response.code))

    jsonStr = un_gz('./temp/2017082816.gz')
    for line in jsonStr:
        print(str(line,encoding='utf-8'))
        print('------')
