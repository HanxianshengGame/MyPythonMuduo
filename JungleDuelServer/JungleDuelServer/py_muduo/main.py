#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/14 16:26
# @Author  : handling
# @File    : main.py
# @Software: PyCharm

import logger
from task import Task
from tcp_server import TcpServer
from compute_threadpool import ComputeThreadPool


def on_connection(conn):
    logger.simple_log('新的玩家连接：', conn.get_peer_addr())
    pass


def on_message(conn):
    msg = conn.recv_msg()
    print msg
    if not msg:
        return False
    compute_thread_pool.add_task(Task(conn, msg))
    return True


def on_close(conn):
    conn.simple_log(conn.get_peer_addr(), ' close!')





class GameServer:

    def __init__(self, ip, port):
        self.__compute_thread_pool = compute_thread_pool
        self.__server = TcpServer(ip, port, 5)

    def start(self):
        self.__compute_thread_pool.start()
        self.__server.start()

    def stop(self):
        pass


compute_thread_pool = ComputeThreadPool(5, 20)
game_server = GameServer('172.17.47.226', 2000)
game_server.start()
