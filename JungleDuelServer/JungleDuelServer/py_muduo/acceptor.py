# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : acceptor.py
# @Time     : 2021/1/10 19:11
# @Software : PyCharm
# @Introduce: This is

import socket
class Acceptor:

    def __init__(self, ip, port):
        self.__addr = (ip, port)
        self.__listen_sock = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM)
        pass

    def __set_reuse_addr(self):
        self.__listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __set_reuse_port(self):
        self.__listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    def __bind(self):
        self.__listen_sock.bind(self.__addr)

    def __listen(self):
        self.__listen_sock.listen(10)

    def ready(self):
        self.__set_reuse_addr()
        self.__set_reuse_port()
        self.__bind()
        self.__listen()

        # 接收的 socket 配合epoll的话一般是 水平触发 + 非阻塞/阻塞都可以
        self.__listen_sock.setblocking(False)
        pass

    def get_listen_fd(self):
        return self.__listen_sock.fileno()

    def accept(self):
        client_sock, client_addr = self.__listen_sock.accept()
        return client_sock, client_addr


