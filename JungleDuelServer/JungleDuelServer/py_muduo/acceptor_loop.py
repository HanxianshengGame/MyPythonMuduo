#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 10:00
# @Author  : handling
# @File    : acceptor_loop.py
# @Software: PyCharm

import select
import logger
from tcp_connection import TcpConnection


class AcceptorLoop:

    def __init__(self, acceptor):
        self.__acceptor = acceptor
        self.__epoll = select.epoll()
        self.__epoll.register(self.__acceptor.get_listen_fd()
            , select.EPOLLIN)
        pass

    def loop(self, sub_reactors):
        logger.simple_log('正在接受玩家连接')
        while True:
            events = self.__epoll.poll(10)
            if not events:
                logger.simple_log('暂时没有新玩家连接')
                continue
            # 有玩家连接
            for i in range(len(events)):
                client_sock, client_addr = self.__acceptor.accept()

                sub_reactors.assign_new_conn(TcpConnection(client_sock))
        pass
