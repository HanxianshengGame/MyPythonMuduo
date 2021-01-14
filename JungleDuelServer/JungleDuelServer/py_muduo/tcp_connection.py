# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : tcp_connection.py
# @Time     : 2021/1/10 19:26
# @Software : PyCharm
# @Introduce: This is


from socket_message_handler import send_msg_to_client, recv_msg_from_client
from main import on_message, on_connection, on_close


class TcpConnection:
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

    def set_loop_(self, event_loop):
        self.__event_loop = event_loop


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

    def get_socket(self):
        return self.__sock

    def recv_msg(self):
        return recv_msg_from_client(self.__sock)

    def handle_message_callback(self):
        self.__on_message_callback(self)

    def handle_connection_callback(self):
        self.__on_connection_callback(self)

    def handle_close_callback(self):
        self.__on_close_callback(self)
