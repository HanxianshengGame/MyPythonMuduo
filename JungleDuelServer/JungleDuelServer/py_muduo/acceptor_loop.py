#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 10:00
# @Author  : handling
# @File    : acceptor_loop.py
# @Software: PyCharm

import select
import logger
import errno
from tcp_connection import TcpConnection


class AcceptorLoop:

    def __init__(self, acceptor):
        self.__acceptor = acceptor
        self.__epoll = select.epoll()
        self.__epoll.register(self.__acceptor.get_listen_fd()
                              , select.EPOLLIN)
        self.__is_looping = False
        pass

    def un_loop(self):
        if self.__is_looping:
            self.__is_looping = False

    def loop(self, sub_reactors):
        self.__is_looping = True
        logger.simple_log('正在接受玩家连接')
        while self.__is_looping:
            try:
                events = self.__epoll.poll(10)
                if not events:
                    logger.simple_log('暂时没有新玩家连接')
                    continue
                # 有玩家连接
                for i in range(len(events)):
                    client_sock, client_addr = self.__acceptor.accept()

                    sub_reactors.assign_new_conn(TcpConnection(client_sock))
            except IOError as error:
                if error.errno == errno.EINTR:
                    continue
        pass
