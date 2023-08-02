# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/7/18 15:03
# Desc: 模拟对话

import threading
from base.common import *

cond = threading.Condition()


class A(threading.Thread):

    def __init__(self, cond, name):
        threading.Thread.__init__(self, name=name)
        self.cond = cond

    def run(self):
        self.cond.acquire()  # 获取锁
        dp(self.name + '哈喽')
        self.cond.notify()  # 唤醒其他wait状态的线程。(通知另一个人对话)
        self.cond.wait()  # 自己进入等待状态，等待notify通知唤醒。

