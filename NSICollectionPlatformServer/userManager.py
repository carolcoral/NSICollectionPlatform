#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataSource import DataSource
import hashlib


def create_token(message):
    """
    生成随机码
    :param message: 原始报文
    :return: 密文
    """
    m2 = hashlib.md5()
    m2.update(message.encode("utf8"))
    return m2.hexdigest()


class UserManager:
    def __init__(self, host='localhost', port=3306, username=None, password=None, database=None):
        self.db = DataSource(host, port, username, password, database)

    def valid_token(self, token=None):
        sql = 'SELECT `password` FROM USER'
        password_list = self.db.fetchall(sql)
        token_list = []
        for passwd in password_list:
            token_list.append(passwd["password"])
        if token in token_list:
            return True
        else:
            return False

    def valid_login(self, username, password):
        """
        登录验证
        :param username: 用户名
        :param password: 密码
        :return:
        """
        password = create_token(username + password)
        sql = 'SELECT * FROM USER WHERE username="' + username + '" AND password="' + password + '"'
        return self.db.fetchone(sql=sql)

    def user_register(self, username, password, role):
        """
        用户注册
        :param username: 用户名
        :param password: 密码
        :return:
        """
        password = create_token(username + password)
        sql_select = 'SELECT COUNT(1) FROM USER WHERE `username`="' + username + '"'
        count = self.db.fetchone(sql_select)
        if count["COUNT(1)"] >= 1:
            return False
        else:
            sql_insert = 'INSERT INTO USER (`username`, `password`, `role`) VALUES ("' + username + '", "' + password + '", "' + role+'")'
            self.db.execute(sql_insert)
            return True

    def user_add(self, username, password, role):
        password = create_token(username + password)
        sql_select = 'SELECT COUNT(1) FROM USER WHERE `username`="' + username + '"'
        count = self.db.fetchone(sql_select)
        if count["COUNT(1)"] >= 1:
            return False
        else:
            sql_insert = 'INSERT INTO USER (`username`, `password`, `role`) VALUES ("' + username + '", "' + password + '", "' + role + '") '
            self.db.execute(sql_insert)
            return True

    def user_delete(self, user_id):
        sql_delete = 'DELETE FROM USER WHERE `id`="' + str(user_id) + '"'
        self.db.execute(sql_delete)
        return True

    def user_edit(self, user_id, username, password, role):
        password = create_token(username + password)
        sql_edit = 'UPDATE USER SET `password`="' + password + '" WHERE `id`="' + str(user_id) + '"'
        self.db.execute(sql_edit)
        return True

    def user_list(self):
        sql_list = 'SELECT * FROM USER'
        return self.db.fetchall(sql_list)

    def user_get(self, user_id):
        sql_select = 'SELECT * FROM USER WHERE `id`="' + str(user_id) + '"'
        return self.db.fetchone(sql_select)

    def user_authority_change(self, user_id, role):
        sql_edit = 'UPDATE USER SET `role`="' + role + '" WHERE `id`="' + str(user_id) + '"'
        self.db.execute(sql_edit)
        return True
