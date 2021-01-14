# !/usr/bin/env Python2
# -*- coding: utf-8 -*-
# @Author   : 得灵
# @FILE     : type_convert.py
# @Time     : 2021/1/9 10:56
# @Software : PyCharm
# @Introduce: This is

from socket import *
import struct


def int_to_bytes(len):
    format_str = '<i'
    s = struct.Struct(format_str)
    return s.pack(len)


def str_to_bytes(content):
    format_str = '<' + str(len(content)) + 's'
    s = struct.Struct(format_str)
    return s.pack(content)


def bytes_to_int(data):
    format_str = '<i'
    s = struct.Struct(format_str)
    return s.unpack(data)[0]


def bytes_to_str(data, data_len):
    format_str = '<' + str(data_len) + 's'
    s = struct.Struct(format_str)
    return s.unpack(data)[0]


# content = "nihao"
#
# send_data = int_to_bytes(len(content)) + str_to_bytes(content)
# print send_data
#
# data_len = bytes_to_int(send_data[0:4:])
# print data_len

print

