#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import traceback

from dataSource import DataSource


class OperationLog:
    def __init__(self, host='localhost', port=3306, username=None, password=None, database=None):
        self.db = DataSource(host, port, username, password, database)

    def log(self, token, desc="", data=None, username=""):
        """
        记录用户操作
        :param token: 令牌（用户名和令牌不可同时有值）
        :param desc: 操作描述
        :param data: 操作数据
        :param username: 用户名（用户名和令牌不可同时有值）
        """
        try:
            if data is None:
                data = {}
            if "" == token:
                sql_insert = 'INSERT INTO LOG_OPERATION (username, operationContent, operationData) VALUES ("' + username + '", "' + desc + '", ' + json.dumps(
                    json.dumps(data)) + ')'
            else:
                sql = 'SELECT * FROM USER WHERE `password`="' + token + '"'
                user_info = self.db.fetchone(sql)
                sql_insert = 'INSERT INTO LOG_OPERATION (username, operationContent, operationData) VALUES ("' + \
                             user_info["username"] + '", "' + desc + '", ' + json.dumps(json.dumps(data)) + ')'
            self.db.execute(sql=sql_insert)
        except Exception as e:
            traceback.print_exc()

    def list_log(self, username=""):
        """
        获取用户操作列表集合
        :param username: 根据用户名查看对应操作记录
        :return:
        """
        if username is None or username == "":
            sql = 'SELECT * FROM LOG_OPERATION'
        else:
            sql = 'SELECT * FROM LOG_OPERATION WHERE username="' + username + '"'
        return self.db.fetchall(sql)
