#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup


def sub_domain_lookup(domain):
    domain_list = {}
    for n in range(1, 2):
        j = 1
        if n > 1:
            j = n*10-1
        url = "https://cn.bing.com/search?q=domain%3A"+domain+"&qs=n&form=QBLH&sp=-1&pq=domain%3A"+domain+"&sc=1-16&sk=&cvid=EE75884389DB41A8969DA805C55E4F8A"
        # url = "https://cn.bing.com/search?q=domain:" + domain + "&first=" + str(j) + "&go=搜索&qs=ds&FORM=PERE"
        print(url)
        resp = requests.get(url).content
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
    print(sub_domain_lookup("baidu.com"))
