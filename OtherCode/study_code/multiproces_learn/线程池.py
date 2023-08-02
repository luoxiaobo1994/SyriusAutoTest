# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/7/18 15:48
# Desc: 线程池的使用。
import random
from concurrent.futures import ThreadPoolExecutor
import time

num = 0


def func(x):
    global num
    num += 1
    time.sleep(random.random())

executor = ThreadPoolExecutor(max_workers=20)
executor.submit(func,list(range(20)))
print(num)