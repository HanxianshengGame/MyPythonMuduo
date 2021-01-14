#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 11:01
# @Author  : handling
# @File    : client_test.py
# @Software: PyCharm

import socket
import time

client_sock = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)

client_sock.connect(('39.105.35.17', 2000))

count = 5
while count:
    send_sz = client_sock.send('111111')
    print send_sz
    time.sleep(2)
    count -= 1

client_sock.close()
