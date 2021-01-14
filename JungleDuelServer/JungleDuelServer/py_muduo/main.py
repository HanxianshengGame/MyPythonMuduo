#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 16:26
# @Author  : handling
# @File    : main.py
# @Software: PyCharm

from tcp_server import TcpServer
from compute_threadpool import ComputeThreadPool
from tcp_connection import TcpConnection


class GameServer:

    def __init__(self, ip, port):
        self.__compute_thread_pool = compute_thread_pool
        self.__server = TcpServer(ip, port, 5)

    def start(self):
        TcpConnection.compute_thread_pool = compute_thread_pool
        self.__compute_thread_pool.start()
        self.__server.start()

    def stop(self):
        pass


compute_thread_pool = ComputeThreadPool(5, 20)
game_server = GameServer('172.17.47.226', 2000)
game_server.start()
