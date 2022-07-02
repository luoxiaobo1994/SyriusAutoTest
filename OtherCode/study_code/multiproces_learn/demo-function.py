# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/2 0:54
# Desc: 进程相关的函数3

from multiprocessing import Process
import os, time


def foo(x):
    print(f"foo-x:{x}")


if __name__ == '__main__':
    p = Process(name='demo', target=foo, args=(1,))
    # 设置为守护进程，默认为False
    p.daemon = True
    # 启动子进程
    p.start()
    # 输出子进程的名称
    print(p.name)
    # 输出子进程ID
    print(p.pid)
    # 判断子进程是否还存活
    print(p.is_alive())
    # 终止子进程
    p.kill()
    # 终止子进程
    p.terminate()
    # 输出子进程的退出码
    print(p.exitcode)
    # 关闭Process对偶性，释放占用的资源
    p.close()

