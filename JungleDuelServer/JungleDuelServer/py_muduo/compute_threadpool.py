#!/usr/bin/env python27
# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 10:01
# @Author  : handling
# @File    : compute_threadpool.py
# @Software: PyCharm

from compute_thread import ComputeThread
from Queue import Queue
from time import sleep


class ComputeThreadPool:
    def __init__(self, thread_num, task_que_sz):
        self.__thread_num = thread_num
        self.__task_que_sz = task_que_sz
        self.__is_exit = False
        self.__compute_threads = []
        self.__task_que = Queue(task_que_sz)

        pass

    def add_task(self, task):
        self.__task_que.put(task, True)

    def get_task(self):
        return self.__task_que.get(True)

    def stop(self):
        if not self.__is_exit:
            while not self.__task_que.empty():
                sleep(1)
            self.__is_exit = True
            for compute_thread in self.__compute_threads:
                compute_thread.join()


    def start(self):
        for i in range(self.__thread_num):
            compute_thread = ComputeThread('thread' + str(i),
                self.thread_func, ())
            self.__compute_threads.append(compute_thread)

        for compute_thread in self.__compute_threads:
            compute_thread.start()

    def thread_func(self):
        while not self.__is_exit:
            task = self.get_task()
            task.process()
