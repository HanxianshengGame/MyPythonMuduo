# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : tcp_connection.py
# @Time     : 2021/1/10 19:26
# @Software : PyCharm
# @Introduce: This is
import logger
from task import Task
from socket_message_handler import send_msg_to_client, recv_msg_from_client


def on_connection(conn):
    logger.simple_log('新的玩家连接：', conn.get_peer_addr())
    pass


def on_message(conn):
    msg = conn.recv_msg()
    logger.simple_log(conn.get_peer_addr(), "发来了消息：", msg)
    if not msg:
        return False
    TcpConnection.compute_thread_pool.add_task(Task(conn, msg))
    return True


def on_close(conn):
    logger.simple_log(conn.get_peer_addr(), ' close!')


class TcpConnection:
    compute_thread_pool = None
    __on_connection_callback = on_connection
    __on_message_callback = on_message
    __on_close_callback = on_close

    def __init__(self, client_sock):
        self.__sock = client_sock
        self.__event_loop = None
        """
        IO socket 搭配epoll 一般是非阻塞+边缘触发ET
        """
        self.__sock.setblocking(False)
        self.__local_addr = client_sock.getsockname()
        self.__peer_addr = client_sock.getpeername()

        pass

    def set_loop(self, event_loop):
        self.__event_loop = event_loop

    def recv_msg(self):
        return recv_msg_from_client(self.__sock)

    def send_msg(self, msg):
        send_msg_to_client(self.__sock, msg)

    def send_in_loop(self, msg):
        if self.__event_loop:
            self.__event_loop.run_in_loop(self.send_msg, msg)

    def close(self):
        self.__sock.close()

    def get_peer_addr(self):
        return self.__peer_addr

    def get_fd(self):
        return self.__sock.fileno()

    def handle_message_callback(self):
        return TcpConnection.__on_message_callback(self)

    def handle_connection_callback(self):
        TcpConnection.__on_connection_callback(self)

    def handle_close_callback(self):
        TcpConnection.__on_close_callback(self)
