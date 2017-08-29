#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import pymysql


class DB:
    def __init__(self, config):
        # 打开数据库连接
        db_host = config.get("db", "db_host")
        db_user = config.get("db", "db_user")
        db_password = config.get("db", "db_password")
        db_database = config.get("db", "db_database")
        self.table = db_table = config.get("db", "db_table")

        try:
            self.db = pymysql.connect(host=db_host, user=db_user, password=db_password,db=db_database)
        except:
            print('连接数据库失败')


    def zcx(self, c):
        print('sss' + c)

    def insert(self,args):
        db = self.db
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        sql = "CREATE TABLE IF NOT EXISTS "+self.table+" ( " \
              "`id` int(10) unsigned NOT NULL AUTO_INCREMENT, " \
              "`msg_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '消息id', " \
              "`timestamp` varchar(13) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '消息id', " \
              "`direction` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '方向', " \
              "`to` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '接受人用户名', " \
              "`from` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '发送人用户名', " \
              "`chat_type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '单聊还是群聊', " \
              "`payload` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '消息体', " \
              "`created_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00', " \
              "`updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00', " \
              "PRIMARY KEY (`id`), KEY `history_messages_to_index` (`to`), " \
              "KEY `history_messages_from_index` (`from`) " \
              ") ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci"
        sql = sql.encode("utf-8").decode("latin1")
        cursor.execute(sql)
        # SQL 插入语句
        sql = "INSERT INTO "+self.table+"( `msg_id`, `timestamp`, `direction`, `to`, `from`, `chat_type`, " \
              "`payload`, `created_at`, `updated_at`) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            # 执行sql语句
            cursor.executemany(sql, args)
            # 执行sql语句
            db.commit()
        except Exception as e:
            # 发生错误时回滚
            db.rollback()
            print('插入失败')
            print(e)
        finally:
            # 关闭数据库连接
            db.close()
