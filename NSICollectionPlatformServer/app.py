#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import Flask
from flask import request, make_response

import userManager as User
import dnsResolve
import subdomainLookup
import emailGrabbing
import portDetection
import logOperation as Operation

app = Flask(__name__)

data_source = {
    "host": "118.24.151.27",
    "username": "admin",
    "password": "Liu947752894!",
    "database": "NSI"
}
logOperation = Operation.OperationLog(**data_source)
user_manager = User.UserManager(**data_source)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)


def result(code="000000", desc="SUCCESS", data=None):
    res = {
        "code": code,
        "desc": desc,
        "data": data
    }
    return res


@app.before_request
def request_handle():
    """
    请求拦截器，根据token统一判断是否可用
    :return: 拦截结果
    """
    print(request.url)
    print(request.headers)
    url = request.url.split("/admin")[1]
    print(url)
    url = url.split("?")[0]
    print(url)
    if url not in ["/login", "/register"]:
        flag = False
        if "token" in request.headers:
            token = request.headers['token']
            flag = user_manager.valid_token(token)
        if not flag:
            response = make_response(result(code="100000", desc="valid token error"))
            response.status = 401
            return response


def log_operation(request_info, desc="", data=None):
    """
    记录操作日志记录并保存在数据库中
    :param request_info: 请求命令
    :param desc: 用户执行的操作
    :param data: 操作执行数据内容
    """
    token = ""
    username = ""
    if "token" in request_info.headers \
            and request_info.headers["token"] is not None \
            and 'null' != request_info.headers["token"]:
        token = request_info.headers["token"]
    else:
        username = request_info.json["username"]
    logOperation.log(token=token, desc=desc, data=data, username=username)


@app.route('/admin/login', methods=['POST'])
def login():
    """
    用户登录
    :return: 登录结果
    """
    username = request.json['username']
    password = request.json['password']
    __res = user_manager.valid_login(username, password)
    if __res is None or len(__res) == 0:
        res = result(code="10000", desc="用户不存在")
    else:
        data = {
            "token": User.create_token(username + password),
            "role": __res['role']
        }
        res = result(data=data)
    log_operation(request_info=request, desc="用户登录", data={
        "用户名": username,
        "操作执行结果": res
    })
    return res


@app.route('/admin/register', methods=['POST'])
def register():
    """
    用户注册，此时无法设置权限，只能管理员对用户设置权限
    :return:
    """
    username = request.json['username']
    password = request.json['password']
    role = request.json['role']
    __res = user_manager.user_register(username, password, role)
    if __res:
        res = result(data="用户注册成功")
    else:
        res = result(code="10000", desc="用户已经存在")
    log_operation(request_info=request, desc="用户注册", data={
        "用户名": username,
        "操作执行结果": res
    })
    return res


@app.route('/admin/user/add', methods=['POST'])
def user_add():
    """
    新增用户
    :return:
    """
    __res = user_manager.user_add(
        request.json['username'],
        request.json['password'],
        request.json['role'],
    )
    if __res:
        res = result(data="新增用户成功")
    else:
        res = result(code="10000", desc="新增用户失败")
    log_operation(request_info=request, desc="管理员新增用户", data={
        "用户名": request.json['username'],
        "角色": request.json['role'],
        "操作执行结果": res
    })
    return res


@app.route('/admin/user/delete', methods=['POST'])
def user_delete():
    """
    根据id删除用户
    :return:
    """
    __id = request.json['id']
    __res = user_manager.user_delete(__id)
    if __res:
        res = result(data="删除用户成功")
    else:
        res = result(code="10000", desc="删除用户失败")
    log_operation(request_info=request, desc="删除用户", data={
        "ID": __id,
        "操作结果": res
    })
    return res


@app.route('/admin/user/edit', methods=['POST'])
def user_edit():
    """
    编辑用户
    :return:
    """
    __res = user_manager.user_edit(
        request.json['id'],
        request.json['username'],
        request.json['password'],
        request.json['role'],
    )
    if __res:
        res = result(data="编辑用户成功")
    else:
        res = result(code="10000", desc="编辑用户失败")
    log_operation(request_info=request, desc="编辑用户", data={
        "ID": request.json['id'],
        "用户名": request.json['username'],
        "角色": request.json['role'],
        "操作执行结果": res
    })
    return res


@app.route('/admin/user/list', methods=['GET'])
def user_list():
    """
    获取用户列表
    :return:
    """
    __res = user_manager.user_list()
    if __res:
        return result(data=__res)
    else:
        return result(code="10000", desc="获取用户列表失败")


@app.route('/admin/user/get', methods=['GET'])
def user_get():
    """
    根据id获取用户信息
    :return:
    """
    __res = user_manager.user_get(request.values['id'])
    if __res:
        return result(data=__res)
    else:
        return result(code="10000", desc="获取用户信息失败")


@app.route('/admin/user/authority/change', methods=['POST'])
def user_authority_change():
    """
    根据id修改用户权限
    :return:
    """
    __id = request.json['id']
    __role = request.json['role']
    __res = user_manager.user_authority_change(__id, __role)
    if __res:
        res = result(data=__res)
    else:
        res = result(code="10000", desc="获取用户信息失败")
    log_operation(request_info=request, desc="修改用户权限", data={
        "ID": __id,
        "角色": __role,
        "操作执行结果": res
    })
    return res


@app.route('/admin/dns/resolution', methods=['GET'])
def dns_resolution():
    """
    DNS解析
    :return:
    """
    __domainType = request.values["domainType"]
    __domain = request.values["domain"]
    if __domainType is None or __domainType not in ["A", "MX", "NS", "CNAME"]:
        res = result(code="100000", desc="无效类型")
    else:
        if "A" == __domainType:
            __data = dnsResolve.resolution_a(__domain)
        elif "MX" == __domainType:
            __data = dnsResolve.resolution_mx(__domain)
        elif "NS" == __domainType:
            __data = dnsResolve.resolution_ns(__domain)
        elif "CNAME" == __domainType:
            __data = dnsResolve.resolution_cname(__domain)
        else:
            __data = []
        res = result(data=__data)
    log_operation(request_info=request, desc="DNS解析", data={
        "解析类型": __domainType,
        "解析域名": __domain,
        "解析结果": res
    })
    return res


@app.route('/admin/subdomain/lookup', methods=['GET'])
def subdomain_lookup():
    """
    子域名查询
    :return:
    """
    domain = request.values["domain"]
    if domain is None or domain == "":
        res = result(code="100000", desc="域名为空")
    else:
        sub_domain_list = subdomainLookup.sub_domain_lookup(domain=domain)
        __data = []
        for key in sub_domain_list:
            __data.append({
                "href": key,
                "title": sub_domain_list[key]
            })
        res = result(data=__data)
    log_operation(request_info=request, desc="子域名查询", data={
        "解析域名": domain,
        "解析结果": res
    })
    return res


@app.route('/admin/email/grabbing', methods=['GET'])
def email_grabbing():
    """
    邮箱账号抓取
    :return:
    """
    keyword = request.values["keyword"]
    email_suffix = request.values["email_suffix"]
    email_count = int(request.values["email_count"])
    if keyword is None or keyword == "":
        res = result(code="100000", desc="搜索关键值不能为空")
    elif email_suffix is None or email_suffix == "":
        res = result(code="100000", desc="搜索邮箱后缀不能为空")
    else:
        email_grabbing_result = emailGrabbing.EmailAccountGrabbing(keyword=keyword, email_suffix=email_suffix,
                                                                   email_count=email_count).grabbing()
        res = result(data=email_grabbing_result)
    log_operation(request_info=request, desc="邮箱账号抓取", data={
        "查询关键字": keyword,
        "指定邮箱后缀": email_suffix,
        "邮箱账号抓取结果": res
    })
    return res


@app.route('/admin/port/detection', methods=['GET'])
def port_detection():
    """
    端口检测
    :return:
    """
    domain = request.values["domain"]
    port = request.values["port"]
    if domain is None or domain == "":
        res = result(code="100000", desc="域名/IP不能为空")
    else:
        port_detection_result = portDetection.detection(domain=domain, port=port)
        res = result(data=port_detection_result)
    log_operation(request_info=request, desc="端口检测", data={
        "域名或IP": domain,
        "端口号": port,
        "执行结果": res
    })
    return res


@app.route('/admin/operation/log/get', methods=['GET'])
def operation_log():
    """
    操作记录
    :return:
    """
    username = request.values["username"]
    __operation_log_list = logOperation.list_log(username=username)
    res = result(data=__operation_log_list)
    return res
