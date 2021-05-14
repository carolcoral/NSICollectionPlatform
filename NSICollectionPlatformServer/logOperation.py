#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from dataSource import DataSource

db = DataSource(host="118.24.151.27", username="admin", password="Liu947752894!", database="NSI")


def log(token, desc="", data=None):
    if data is None:
        data = {}
    sql = 'SELECT * FROM USER WHERE `password`="' + token + '"'
    user_info = db.fetchone(sql)
    sql_insert = 'INSERT INTO LOG_OPERATION (username, operationcontent, operationdata) VALUES ("' + user_info[
        "username"] + '", "' + desc + '", "' + json.dumps(data) + '")'
    db.execute(sql=sql_insert)


def list_log(username=""):
    if username is None or username == "":
        sql = 'SELECT * FROM LOG_OPERATION'
    else:
        sql = 'SELECT * FROM LOG_OPERATION WHERE username="' + username + '"'
    return db.fetchall(sql)
