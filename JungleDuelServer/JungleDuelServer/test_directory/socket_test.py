# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : socket_test.py
# @Time     : 2021/1/9 14:45
# @Software : PyCharm
# @Introduce: This is
import select
import Queue
import struct
import errno
import socket


def int_to_bytes(convert_val):
    format_str = '<i'
    s = struct.Struct(format_str)
    return s.pack(convert_val)


def str_to_bytes(convert_val):
    format_str = '<' + str(len(convert_val)) + 's'
    s = struct.Struct(format_str)
    return s.pack(convert_val)


def bytes_to_int(convert_data):
    format_str = '<i'
    s = struct.Struct(format_str)
    return s.unpack(convert_data)[0]


def bytes_to_str(convert_data, data_len):
    format_str = '<' + str(data_len) + 's'
    s = struct.Struct(format_str)
    return s.unpack(convert_data)[0]


def recv_fixed_sz_data(sock, recv_sz):
    total = 0
    result_data = ''
    while total < recv_sz:
        data = sock.recv(recv_sz - total)
        if data:
            result_data += data
            total += len(data)
        else:
            return int_to_bytes(0)
    return result_data


def recv_client_msg(sock):
    data_len = bytes_to_int(recv_fixed_sz_data(sock, 4))
    if not data_len:
        return None
    msg = bytes_to_str(recv_fixed_sz_data(sock, data_len), data_len)
    if not msg:
        return None
    return msg


server_sock = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server_addr = ('172.17.47.226', 2000)
server_sock.bind(server_addr)
server_sock.listen(10)

print '服务器启动成功， 监听IP：', server_addr

server_sock.setblocking(True)

timeout = 10

epoll = select.epoll()

# epoll 注册监听事件
epoll.register(server_sock.fileno(), select.EPOLLIN)

message_queues = {}
fd_to_socket = {server_sock.fileno(): server_sock}
buffer_sz = 1024

while True:
    print '等待活动连接：.......'
    events = epoll.poll(timeout)
    if not events:
        print 'epoll超时无活动连接，重新轮询......'
        continue
    print "有{0}个新事件，开始处理.....".format(len(events))
    for fd, event in events:
        event_socket = fd_to_socket[fd]
        # 接收新连接事件
        if event_socket == server_sock:
            client_sock, client_addr = server_sock.accept()
            print '新连接：', client_addr
            client_sock.setblocking(False)
            epoll.register(client_sock.fileno(), select.EPOLLIN|select.EPOLLET)
            fd_to_socket[client_sock.fileno()] = client_sock
            message_queues[client_sock] = Queue.Queue()
        # 客户端非正常关闭事件
        elif event & select.EPOLLHUP:
            print '触发了 EPOLLHUP事件'
            print 'client close'.format(event_socket.getpeername())
            epoll.unregister(fd)
            fd_to_socket[fd].close()
            del message_queues[event_socket]
            del fd_to_socket[fd]
        # 可读事件（客户端发来消息）
        elif event & select.EPOLLIN:
            # 正常关闭会触发 EPOLLIN

            try:
                while True:
                    msg = event_socket.recv(10)
                    print msg
                    if not msg:
                        print '对端主动关闭'
                        print 'client: {0} close'.format(event_socket.getpeername())
                        epoll.unregister(fd)
                        fd_to_socket[fd].close()
                        del fd_to_socket[fd]
                        break
            except socket.error as msg:
                print msg.errno
                if msg.errno == errno.EAGAIN:
                    print '已经读完接收缓冲区'
                else:
                    print 'client: {0} close'.format(event_socket.getpeername())
                    epoll.unregister(fd)
                    fd_to_socket[fd].close()
                    del fd_to_socket[fd]

        # 可写事件（）
        elif event & select.EPOLLOUT:
            try:
                msg = message_queues[event_socket].get_nowait()
            except:
                print event_socket.getpeername(), "queue empty"
                epoll.modify(fd, select.EPOLLIN)
            else:
                print "发送数据：", msg, "客户端： ", event_socket.getpeername()
                event_socket.sendall(msg)
    pass

epoll.unregister(server_sock.fileno())
epoll.close()
server_sock.close()
