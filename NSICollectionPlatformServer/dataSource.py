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
import traceback


class DataSource:
    def __init__(self, host='localhost', port=3306, username=None, password=None, database=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        # 打开数据库连接
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.username, password=self.password, database=self.database)
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def __is_connected(self):
        try:
            self.db.ping(reconnect=True)
        except Exception as e:
            traceback.print_exc()
            self.db = pymysql.connections.Connection(host=self.host, port=self.port, user=self.username, password=self.password, database=self.database)

    def fetchall(self, sql):
        self.__is_connected()
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def fetchmany(self, sql):
        self.__is_connected()
        self.cursor.execute(sql)
        return self.cursor.fetchmany()

    def fetchone(self, sql):
        self.__is_connected()
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def execute(self, sql):
        self.__is_connected()
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def close(self):
        self.__is_connected()
        # 关闭数据库连接
        self.db.close()
