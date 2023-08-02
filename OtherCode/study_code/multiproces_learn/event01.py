# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/7/18 14:42
# Desc: 事件和线程

import threading


class MyThread(threading.Thread):

    def __init__(self, event):
        super().__init__()
        self.event = event

    def run(self):
        print(f"线程：{self.name} 已经初始化完成，随时准备启动。")
        self.event.wait()
        print(f"{self.name} 开始执行。")


if __name__ == '__main__':
    event = threading.Event()
    threads = []
    [threads.append(MyThread(event)) for i in range(1, 10)]

    event.clear()

    [t.start() for t in threads]
    event.set()
    [t.join() for t in threads]
