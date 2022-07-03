# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/3 16:56
# Desc: 进程间通讯实例

from multiprocessing import Queue

q = Queue(3)
q.put(1)  # 往队列里塞入一个数据
q.put(2)
q.put(3)
print(q.full())  # 判断进程是否已满。
q.qsize()  # 获取当前队列的大小。
print(q.get())  # 通过get方法，获取成员。 1，先进先出。
print(q.get())  # 2
print(q.get())  # 3

print(q.empty())  # 判断队列是否已经空了
# q.get()  # 空了的情况下，不设置get参数，不会报错。只会阻塞程序。直到顺利get数据。
# q.get(block=False)  # 设置阻塞为False，获取不到，则报错。
q.get(timeout=5)  # 设置超时时间，获取不到，则报错。
