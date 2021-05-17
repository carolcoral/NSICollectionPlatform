#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def __get_http_headers():
    """
    根据不同浏览器组装header请求信息
    :return: header
    """
    try:
        ua = UserAgent()
        header = {
            "User-Agent": ua.random,
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6"
        }
    except Exception as e:
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"}
    return header


def sub_domain_lookup(domain, resolve_count=2):
    """
    子域名解析（默认解析2页）
    :param domain: 域名
    :param resolve_count: 解析页数
    :return: 关联子域名
    """
    domain_list = {}
    for n in range(1, resolve_count):
        j = 1
        if n > 1:
            j = n * 10 - 1
        params = {
            "q": domain,
            "go": "搜索",
            "qs": "n",
            "form": "QBLH",
            "first": j
        }
        cookies = {
            "SRCHHPGUSR": "NRSLT=50"
        }
        res = requests.get("https://cn.bing.com/search", headers=__get_http_headers(), params=params, cookies=cookies)
        resp = res.content
        # BeautifulSoup匹配标题
        html = BeautifulSoup(resp, "html.parser")
        h2_list = html.find_all("h2", {"class": ""})
        for h2 in h2_list:
            if h2.find("a") is not None:
                href = h2.find("a")["href"]
                href = href.split("?")[0]
                domain_list[href] = h2.find("a").text
    return domain_list


if __name__ == '__main__':
    __domain = "baidu.com"
    resolve_result = sub_domain_lookup(domain=__domain)
    print(resolve_result)
