#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2021/05/12
    @Author  :
    @Site    : 
    @File    : dataSource.py
    @Software: PyCharm
    @Description: 
"""
import pymysql
import json


class DataSource:
    def __init__(self, host='localhost', port=3306, username=None, password=None, database=None):
        # 打开数据库连接
        self.db = pymysql.connect(host=host, port=port, user=username, password=password, database=database)
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def fetchall(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def fetchmany(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchmany()

    def fetchone(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def close(self):
        # 关闭数据库连接
        self.db.close()
