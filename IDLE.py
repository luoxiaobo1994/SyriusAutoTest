# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

import time


def tt(timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        pass
    else:
        print("结束了")


tt()
