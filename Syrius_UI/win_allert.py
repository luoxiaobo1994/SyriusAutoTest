# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/8/22 13:47
# Desc: 调用windows系统提示框，方便执行脚本出问题时，及时提醒。

import threading

import win32api
import win32con


def func1():
    win32api.MessageBox(0, '这是一个提示框', 'title', win32con.MB_OK)


t1 = threading.Thread(target=func1, args=())
# t1.join()
t1.start()

print('看看是不是阻塞的')
exit(100)
