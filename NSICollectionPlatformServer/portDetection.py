#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import dns.resolver
import re


def __check_ip(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False


def __resolution_a(domain):
    query_list = []
    a = dns.resolver.resolve(domain, 'A')
    for i in a.response.answer:
        for j in i.items:
            if j.rdtype == 1:
                ip = j.address
                query_list.append(ip)
    return query_list


def __detect_port(ip, port):
    """检测ip上的端口是否开放
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


def detection(domain, port):
    is_ip = __check_ip(domain)
    __data = []
    if is_ip:
        port_status = __detect_port(ip=domain, port=port)
        __data.append({
            "domain": domain,
            "port": port,
            "status": port_status
        })
    else:
        ips = __resolution_a(domain=domain)
        for ip in ips:
            port_status = __detect_port(ip=ip, port=port)
            __data.append({
                "domain": ip,
                "port": port,
                "status": port_status
            })
    return __data
