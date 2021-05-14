#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request, make_response

import userManager
import dnsResolve
import subdomainLookup
import emailGrabbing
import portDetection

app = Flask(__name__)


def result(code="000000", desc="SUCCESS", data=None):
    res = {
        "code": code,
        "desc": desc,
        "data": data
    }
    return res


# @app.before_request
# def request_handle():
#     """
#     请求拦截器，根据token统一判断是否可用
#     :return: 拦截结果
#     """
#     print(request.url)
#     print(request.headers)
#     url = request.url.split("/admin")[1]
#     print(url)
#     url = url.split("?")[0]
#     print(url)
#     if url not in ["/login", "/register"]:
#         flag = False
#         if "token" in request.headers:
#             token = request.headers['token']
#             flag = userManager.valid_token(token)
#         if not flag:
#             response = make_response(result(code="100000", desc="valid token error"))
#             response.status = 401
#             return response


@app.route('/admin/login', methods=['POST'])
def login():
    """
    用户登录
    :return: 登录结果
    """
    __res = userManager.valid_login(request.json['username'], request.json['password'])
    if __res is None or len(__res) == 0:
        return result(code="10000", desc="FAILED", data="用户不存在")
    else:
        data = {
            "token": userManager.create_token(__res['password']),
            "role": __res['role']
        }
        return result(data=data)


@app.route('/admin/register', methods=['POST'])
def register():
    """
    用户注册，此时无法设置权限，只能管理员对用户设置权限
    :return:
    """
    __res = userManager.user_register(request.json['username'], request.json['password'])
    if __res:
        return result(data="用户注册成功")
    else:
        return result(code="10000", desc="FAILED", data="用户已经存在")


@app.route('/admin/user/add', methods=['POST'])
def user_add():
    """
    新增用户
    :return:
    """
    __res = userManager.user_add(
        request.json['username'],
        request.json['password'],
        request.json['role'],
    )
    if __res:
        return result(data="新增用户成功")
    else:
        return result(code="10000", desc="FAILED", data="新增用户失败")


@app.route('/admin/user/delete', methods=['POST'])
def user_delete():
    """
    根据id删除用户
    :return:
    """
    __res = userManager.user_delete(request.json['id'])
    if __res:
        return result(data="删除用户成功")
    else:
        return result(code="10000", desc="FAILED", data="删除用户失败")


@app.route('/admin/user/edit', methods=['POST'])
def user_edit():
    """
    编辑用户
    :return:
    """
    __res = userManager.user_edit(
        request.json['id'],
        request.json['username'],
        request.json['password'],
        request.json['role'],
    )
    if __res:
        return result(data="编辑用户成功")
    else:
        return result(code="10000", desc="FAILED", data="编辑用户失败")


@app.route('/admin/user/list', methods=['GET'])
def user_list():
    """
    获取用户列表
    :return:
    """
    __res = userManager.user_list()
    if __res:
        return result(data=__res)
    else:
        return result(code="10000", desc="FAILED", data="获取用户列表失败")


@app.route('/admin/user/get', methods=['GET'])
def user_get():
    """
    根据id获取用户信息
    :return:
    """
    __res = userManager.user_get(request.values['id'])
    if __res:
        return result(data=__res)
    else:
        return result(code="10000", desc="FAILED", data="获取用户信息失败")


@app.route('/admin/dns/resolution', methods=['GET'])
def dns_resolution():
    """
    DNS解析
    :return:
    """
    __domainType = request.values["domainType"]
    if __domainType is None or __domainType not in ["A", "MX", "NS", "CNAME"]:
        return result(code="100000", desc="FAILED", data="无效类型")
    else:
        __domain = request.values["domain"]
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
        return result(data=__data)


@app.route('/admin/subdomain/lookup', methods=['GET'])
def subdomain_lookup():
    """
    子域名查询
    :return:
    """
    domain = request.values["domain"]
    if domain is None or domain == "":
        return result(code="100000", desc="FAILED", data="域名为空")
    else:
        sub_domain_list = subdomainLookup.sub_domain_lookup(domain=domain)
        __data = []
        for key in sub_domain_list:
            __data.append({
                "href": key,
                "title": sub_domain_list[key]
            })
        return result(data=__data)


@app.route('/admin/email/grabbing', methods=['GET'])
def email_grabbing():
    """
    邮箱账号抓取
    :return:
    """
    keyword = request.values["keyword"]
    email_suffix = request.values["email_suffix"]
    if keyword is None or keyword == "":
        return result(code="100000", desc="FAILED", data="搜索关键值不能为空")
    if keyword is None or keyword == "":
        return result(code="100000", desc="FAILED", data="搜索关键值不能为空")
    email_grabbing_result = emailGrabbing.EmailAccountGrabbing(keyword=keyword, email_suffix=email_suffix).grabbing()
    return result(data=email_grabbing_result)


@app.route('/admin/port/detection', methods=['GET'])
def port_detection():
    """
    端口检测
    :return:
    """
    domain = request.values["domain"]
    if domain is None or domain == "":
        return result(code="100000", desc="FAILED", data="域名/IP为空")
    else:
        port_detection_result = portDetection.detection(domain=domain, port=request.values["port"])
        return result(data=port_detection_result)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
