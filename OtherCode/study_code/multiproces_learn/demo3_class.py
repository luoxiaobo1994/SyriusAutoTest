# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/2 0:20
# Desc: 继承了Process类的另一种实现多进程的方式。2

from multiprocessing import Process
import os


class Foo(Process):
    def __init__(self, name):
       super().__init__()

    def run(self):
        print(f"name:{self.name}")
        print(f"sub process:{os.getpid()}")

if __name__ == '__main__':
    print(f"parent process:{os.getpid()}")
    p = Foo('bob')
    p.start()
