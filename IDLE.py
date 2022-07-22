# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

import time


def xx():
    global x
    x = 5


def tt(timeout=0):
    start = time.time()
    while time.time() - start < timeout:
        pass
    else:
        print(f"结束了:{x}")


print(__file__)
