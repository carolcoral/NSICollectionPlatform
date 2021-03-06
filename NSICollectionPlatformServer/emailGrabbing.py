#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_http_headers():
    try:
        ua = UserAgent()
        header = {
            "User-Agent": ua.random,
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6"
        }
    except Exception as e:
        header = {
            u'User-Agent': u'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'}
    return header


class EmailAccountGrabbing:
    def __init__(self, keyword="test", email_count=2, grabbing_engine="https://www.bing.com/search", email_suffix="hotmail.com"):
        """
        邮箱账号抓取初始化
        :param keyword: 关键字，不能为空，例如行业关键字、内容关键字等
        :param email_count: 抓取页数，默认每页10条信息，总抓取账号数<=email_count*10，需要注意email_count过大会导致连接超时
        :param grabbing_engine: 抓取账号的搜索引擎，默认为bing引擎，可以修改为google的引擎，但是修改后需要配置代理，否则无法正常访问
        :param email_suffix: 邮箱后缀，用户过滤账号使用。例如: qq.com / hotmail.com
        """
        self.keyword = keyword
        self.email_count = email_count
        self.grabbing_engine = grabbing_engine
        self.email_suffix = email_suffix

    def grabbing(self):
        """
        账号抓取服务
        :return: .
        """
        email_grabbing_result = []
        for i in range(1, self.email_count):
            j = 1
            if i != 1:
                j = i*10+1
            params = {
                "q": "%s @%s" % (self.keyword, self.email_suffix),
                "go": "搜索",
                "qs": "bs",
                "form": "QBRE",
                "first": j
            }
            cookies = {
                "SRCHHPGUSR": "NRSLT=50"
            }
            ret = requests.get(self.grabbing_engine, headers=get_http_headers(), params=params, cookies=cookies)
            soup = BeautifulSoup(ret.text, "html.parser")
            nodes = soup.find_all(class_="b_caption")
            re_email = re.compile('\w+[a-zA-Z0-9_.\-]*@%s' % self.email_suffix)
            for node in nodes:
                emails = re_email.findall(node.text)
                for email in emails:
                    email_grabbing_result.append({
                        "grabbingEngine": ret.url,
                        "emailAddress": email,
                        "keyword": self.keyword
                    })
        return email_grabbing_result


if __name__ == '__main__':
    grabbing_result = EmailAccountGrabbing(keyword="led", email_suffix="qq.com").grabbing()
    print(grabbing_result)
