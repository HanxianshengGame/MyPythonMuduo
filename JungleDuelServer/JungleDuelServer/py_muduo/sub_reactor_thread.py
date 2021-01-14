#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 9:56
# @Author  : handling
# @File    : sub_reactor_thread.py
# @Software: PyCharm

import logger
from threading import Thread
from event_loop import EventLoop
from socket_message_handler import Flag


class SubReactorThread(Thread):
    def __init__(self, name,  common_conn_que):
        Thread.__init__(self)
        self.name = name
        self.common_conn_que = common_conn_que
        self.__loop = EventLoop(self.get_new_conn, self.get_conn, self.remove_conn)
        self.__fd_to_conns = {}




    def get_new_conn(self):
        new_conn = self.common_conn_que.get(1)
        self.__fd_to_conns[new_conn.get_fd()] = new_conn
        return new_conn

    def wake_up_loop(self):
        """
        唤醒loop去添加新连接的事件描述符
        :return:
        """
        self.__loop.wake_up_self(flag=Flag.ADD_NEW_CONN_EVENT)
        pass

    def get_conn(self, fd):
        return self.__fd_to_conns[fd]

    def remove_conn(self, fd):
        del self.__fd_to_conns[fd]


    def run(self):
        logger.simple_log('正在运做')
        self.__loop.loop()

    def get_conn_count(self):
        return len(self.__fd_to_conns.keys())
