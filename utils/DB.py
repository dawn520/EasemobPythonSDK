#!/usr/bin/python3

import pymysql

class DB:

    def __init__(self,config):
        # 打开数据库连接
        db_host = config.get("db", "db_host")
        db_port = config.getint("db", "db_port")
        db_user = config.get("db", "db_user")
        db_pass = config.get("db", "db_pass")
        self.db = pymysql.connect(db_host, db_user, db_pass, db_pass)

    def insert(self):
        db = self.db
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 插入语句
        sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
               LAST_NAME, AGE, SEX, INCOME) \
               VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
              ('Mac', 'Mohan', 20, 'M', 2000)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
        # 关闭数据库连接
        db.close()
