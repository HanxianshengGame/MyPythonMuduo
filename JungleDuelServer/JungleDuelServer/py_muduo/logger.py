#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 15:41
# @Author  : handling
# @File    : logger.py
# @Software: PyCharm

from threading import current_thread


def simple_log(*args):
    print current_thread().name + ':',
    for i in range(len(args)):
        print args[i],
    print ''
