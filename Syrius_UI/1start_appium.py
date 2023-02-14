# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/1/5 9:02

import os
import time
from multiprocessing.dummy import Pool

from base.common import get_devices

num = len(get_devices())  # 获取当前电脑连接的所有安卓设备.
if num:
    print(f"共有{num}个设备。")
    ls = [4725 + i * 5 for i in range(num)]  # 端口号,每个端口差值是5,
else:
    print("还没有连接任何设备，请先检查一下。")
    exit(100)


def start_appium(port):
    os.system(f"appium -p {port}")
    time.sleep(1)


p = Pool(num)
p.map(start_appium, ls)  # 开完就阻塞了，不会往下走。不过这边的任务也只是开启.后面就不需要管了.
