# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/2 0:13
# Desc: 11

from multiprocessing import Process
from time import sleep


def foo(num):
    print(f"foo-num:{num}")
    sleep(1)


if __name__ == '__main__':
    mp = []
    for i in range(5):
        p = Process(target=foo, args=(i,))
        mp.append(p)
        p.start()
        # p.join()  # 不能在这直接就起来，会阻塞后面的线程。

    for p in mp:
        p.join()  # 应该在这里起来。
