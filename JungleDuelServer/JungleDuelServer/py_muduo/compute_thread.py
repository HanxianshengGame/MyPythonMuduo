#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 10:02
# @Author  : handling
# @File    : compute_thread.py
# @Software: PyCharm

from threading import Thread


class ComputeThread(Thread):
    def __init__(self, name, thread_func, args):
        Thread.__init__(self)
        self.name = name
        self.__func = thread_func
        self.__args = args
        pass

    def run(self):
        self.__func(*self.__args)

