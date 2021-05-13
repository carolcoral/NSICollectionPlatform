#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataSource import DataSource
import hashlib

db = DataSource(host="118.24.151.27", username="admin", password="Liu947752894!", database="NSI")


def create_token(message):
    """
    生成随机码
    :param message: 原始报文
    :return: 密文
    """
    m2 = hashlib.md5()
    m2.update(message.encode("utf8"))
    return m2.hexdigest()


def valid_token(token=None):
    sql = 'SELECT `password` FROM USER'
    password_list = db.fetchall(sql)
    token_list = []
    for passwd in password_list:
        token_list.append(passwd["password"])
    if token in token_list:
        return True
    else:
        return False


def valid_login(username, password):
    """
    登录验证
    :param username: 用户名
    :param password: 密码
    :return:
    """
    password = create_token(password)
    sql = 'SELECT * FROM USER WHERE username="' + username + '" AND password="' + password + '"'
    return db.fetchone(sql=sql)


def user_register(username, password):
    """
    用户注册
    :param username: 用户名
    :param password: 密码
    :return:
    """
    password = create_token(password)
    print(password)
    sql_select = 'SELECT COUNT(1) FROM USER WHERE `username`="' + username + '" AND `password`="' + password + '"'
    count = db.fetchone(sql_select)
    if count["COUNT(1)"] >= 1:
        return False
    else:
        sql_insert = 'INSERT INTO USER (`username`, `password`) VALUES ("' + username + '", "' + password + '")'
        db.execute(sql_insert)
        return True


def user_add(username, password, role):
    password = create_token(password)
    sql_select = 'SELECT COUNT(1) FROM USER WHERE `username`="' + username + '" AND `password`="' + password + '"'
    count = db.fetchone(sql_select)
    if count >= 1:
        return False
    else:
        sql_insert = 'INSERT INTO USER (`username`, `password`, `role`) VALUES ("' + username + '", "' + password + '", "' + role + '") '
        db.execute(sql_insert)
        return True


def user_delete(user_id):
    sql_delete = 'DELETE FROM USER WHERE `id`="' + user_id + '"'
    db.execute(sql_delete)
    return True


def user_edit(user_id, username, password, role):
    password = create_token(password)
    sql_edit = 'UPDATE USER SET `username`="' + username + '", `password`="' + password + '", `role`="' + role + '" WHERE `id`="' + user_id + '"'
    db.execute(sql_edit)
    return True


def user_list():
    sql_list = 'SELECT * FROM USER'
    return db.fetchall(sql_list)


def user_get(user_id):
    sql_select = 'SELECT * FROM USER WHERE `id`="' + user_id + '"'
    return db.fetchone(sql_select)
