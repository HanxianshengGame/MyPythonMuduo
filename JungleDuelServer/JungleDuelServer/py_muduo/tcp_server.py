# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : tcp_server.py
# @Time     : 2021/1/10 19:44
# @Software : PyCharm
# @Introduce: This is

from sub_reactor_threadpool import SubReactorThreadPool
from acceptor import Acceptor
from acceptor_loop import AcceptorLoop




class TcpServer:
    def __init__(self, ip, port, sub_reactor_num):
        self.__acceptor = Acceptor(ip, port)
        self.__loop = AcceptorLoop(self.__acceptor)
        self.__sub_reactors = SubReactorThreadPool(sub_reactor_num)
        pass

    def start(self):
        self.__sub_reactors.start()
        self.__acceptor.ready()
        self.__loop.loop(self.__sub_reactors)
        pass




    def close(self):
        pass


