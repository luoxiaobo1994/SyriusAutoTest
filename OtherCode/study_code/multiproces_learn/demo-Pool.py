# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/2 0:25
# Desc: 进程池4

from multiprocessing import Pool  # 这里导入的是进程池
import time


def foo(num):
    print(f"doo-num:{num}")
    time.sleep(1)


if __name__ == '__main__':
    start = time.time()
    with Pool(20) as p:  # 新写法，以前不知道的。
        p.map(foo, range(100))
    print(f"运行时间：{time.time() - start:.2f}")
