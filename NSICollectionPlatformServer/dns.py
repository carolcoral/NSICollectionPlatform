#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dns


def resolution_a(domain):
    A = dns.resolver.query(domain, 'A')
    for i in A.response.answer:
        for j in i.items:
            print(j.address)

if __name__ == '__main__':
    resolution_a("www.google.com")