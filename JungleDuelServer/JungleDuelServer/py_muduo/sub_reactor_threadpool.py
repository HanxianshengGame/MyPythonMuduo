# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : sub_reactor_threadpool.py
# @Time     : 2021/1/10 20:55
# @Software : PyCharm
# @Introduce: This is

import logger
from Queue import Queue
from sub_reactor_thread import SubReactorThread


class SubReactorThreadPool:


    def __init__(self, thread_num, ):
        self.__thread_num = thread_num
        self.__reactors = []
        self.__conn_que = Queue(10)

        pass

    def start(self):
        for i in range(self.__thread_num):
            reactor = SubReactorThread('reactor' + str(i), self.__conn_que)
            self.__reactors.append(reactor)

        for reactor in self.__reactors:
            reactor.start()

    def stop(self):
        pass


    def assign_new_conn(self, conn):
        logger.simple_log('正在分配新连接')
        self.__conn_que.put(conn, True)
        reactor = min(self.__reactors, key=lambda reactor: reactor.get_conn_count())
        reactor.wake_up_loop()
        pass

