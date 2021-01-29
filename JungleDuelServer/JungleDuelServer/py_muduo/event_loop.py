#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 10:01
# @Author  : handling
# @File    : event_loop.py
# @Software: PyCharm
import select
import logger
import errno
import socket
from socket_message_handler import Flag, recv_flag, send_flag
from threading import Lock


class EventLoop:

    def __init__(self, get_new_conn_func, get_conn_func,
                 remove_conn_func):
        self.__read_sock, self.__write_sock = socket.socketpair(
            socket.AF_UNIX, socket.SOCK_STREAM)

        self.__get_new_conn_func = get_new_conn_func
        self.__get_conn_func = get_conn_func
        self.__remove_conn_func = remove_conn_func

        self.__lock = Lock()
        self.__send_funcs = []  # 存放了自身所管理的连接的未处理的发送事件
        self.__epoll = select.epoll()
        self.__register_listen_fd(self.__read_sock.fileno())
        self.__is_looping = False

    def __register_listen_fd(self, fd):
        self.__epoll.register(fd, select.EPOLLIN | select.EPOLLET)

    def __unregister_listen_fd(self, fd):
        self.__epoll.unregister(fd)

    def __handle_conn_close(self, fd):
        self.__unregister_listen_fd(fd)
        self.__get_conn_func(fd).close()
        self.__remove_conn_func(fd)

    def run_in_loop(self, send_func, msg):
        self.__lock.acquire(True)
        self.__send_funcs.append((send_func, msg))
        self.__lock.release()
        self.wake_up_self(Flag.SEND_MSG_TO_CLIENT)

    def do_send_funcs(self):
        self.__lock.acquire(True)
        tmp = self.__send_funcs
        self.__send_funcs = []
        self.__lock.release()
        for send_func, msg in tmp:
            send_func(msg)

    def wake_up_self(self, flag):
        send_flag(self.__write_sock, flag=flag)
        pass

    def un_loop(self):
        if self.__is_looping:
            self.__is_looping = False

    def loop(self):
        # 监听read_sock 并执行 添加新连接的事件
        self.__is_looping = True
        while self.__is_looping:
            try:
                events = self.__epoll.poll(10)
                if not events:
                    logger.simple_log('暂时没有客户端进行通信')
                    continue
                # 有消息接收
                for fd, event in events:
                    # 表示被分配了新连接
                    if fd == self.__read_sock.fileno():
                        flag = recv_flag(read_sock=self.__read_sock)

                        if flag == Flag.ADD_NEW_CONN_EVENT:
                            new_conn = self.__get_new_conn_func()
                            self.__register_listen_fd(new_conn.get_fd())
                            logger.simple_log('分配到了新连接： ', new_conn.get_peer_addr())

                        elif flag == Flag.SEND_MSG_TO_CLIENT:
                            self.do_send_funcs()
                        else:
                            pass
                    else:
                        conn = self.__get_conn_func(fd)
                        # 有消息来了
                        if event & select.EPOLLIN:
                            try:
                                while True:
                                    need_close = conn.handle_message_callback()
                                    if need_close:
                                        conn.handle_close_callback()
                                        self.__handle_conn_close(fd)
                                        break

                            except socket.error as error_msg:
                                if error_msg.errno != errno.EAGAIN:
                                    print error_msg.errno
                                    conn.handle_close_callback()
                                    self.__handle_conn_close(fd)

                        elif event & select.EPOLLHUP:
                            conn.handle_close_callback()
                            self.__handle_conn_close(fd)
                            pass
            except IOError as error:
                if error.errno == errno.EINTR:
                    continue
