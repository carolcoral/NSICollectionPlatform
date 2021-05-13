#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import dns.resolver
import requests


def resolution_a(domain):
    query_list = []
    a = dns.resolver.query(domain, 'A')
    for i in a.response.answer:
        for j in i.items:
            if j.rdtype == 1:
                ip = j.address
                __ip_query = get_ip_info(ip)
                __ip_query["ip"] = ip
                __ip_query["domain"] = domain
                query_list.append(__ip_query)
    return query_list


def resolution_mx(domain):
    mx = dns.resolver.query(domain, 'MX')  # 指定查看类型为MX
    for i in mx:
        print('MX preference=', i.preference, 'mail exchanger=', i.exchange)


def resolution_ns(domain):
    ns = dns.resolver.query(domain, 'NS')  # 指定查询类型为NS记录
    for i in ns.response.answer:
        for j in i.items:
            print(j.to_text())


def resolution_cname(domain):
    cname = dns.resolver.query(domain, 'CNAME')  # 指定查询类型为CNAME记录
    for i in cname.response.answer:  # 结果将回应cname后的目标域名
        for j in i.items:
            print(j.to_text())


def get_ip_info(ip):
    # IP地址库接口
    r = requests.get('https://ip.taobao.com/getIpInfo.php?ip=%s' % ip)
    content = json.loads(r.content.decode("utf8"))
    ip_query = {}
    if "code" in content and content["code"] == '0':
        i = content['data']
        ip_query["country"] = i['COUNTRY_CN']
        ip_query["area"] = i['AREA_CN']
        ip_query["province"] = i['PROVINCE_CN']
        ip_query["city"] = i['CITY_CN']
        ip_query["isp"] = i['ISP_CN']
    return ip_query


if __name__ == '__main__':
    print(resolution_a("www.baidu.com"))
