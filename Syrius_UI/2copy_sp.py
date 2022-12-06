# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/1/5 15:18

import os
import shutil
import time

from base.common import get_devices

"""快速生成SpeedPicker多个副本的文件。"""

file = "SpeedPicker_cn1.py"  # 确保这个脚本和SpeedPicker_cn1.py在同级目录下.
devices = len(get_devices())


def add_sp(num):
    # 批量复制SP文件。从2开始，因为1是默认那个。
    for n in range(2, num + 1):  # 直接整，重复了也会直接覆盖。
        shutil.copyfile(file, file.split("\\")[-1].replace('1', str(n)))
    print(f"新增文件完成,新增{num - 1}份脚本。")
    time.sleep(1)


def del_sp(num=30):
    # 批量删除SP文件。从2开始，因为1是默认那个。
    for n in range(2, num + 1):
        try:
            os.remove(file.split("\\")[-1].replace('1', str(n)))
        except:
            pass
    print("删除多余文件完成.")
    time.sleep(1)


# del_sp()  # 删除speedpicker_cnx.py
add_sp(devices)  # 复制speedpicker_cnx.py
