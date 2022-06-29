# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/2/10 10:19


import os

from utils.log import logger


def get_devices():
    all_devices = []
    cmd = 'adb devices'
    result = os.popen(cmd).readlines()[1:]
    for item in result:
        if item != "\n":
            all_devices.append(str(item).split("\t")[0])
    # print(get_time(),f"当前连接的设备有：{len(all_devices)}")
    return all_devices


def reset_keyboard(device):
    try:
        tmp_keyboard = os.popen(f"adb -s {device} shell ime list -s").readlines()
        # ['com.baidu.input_huawei/.ImeService\n', 'io.appium.settings/.UnicodeIME\n']
        input_keyboard = [i.replace('\n', '') for i in tmp_keyboard if 'io.appium.settings' not in i]
        os.system(f"adb -s {device} shell ime set {input_keyboard[0]}")
        logger.debug(f"设置设备:{device}的输入法为:{input_keyboard[0]}")
    except:
        logger.debug(f"恢复设备{device}的输入法失败.或设备未连接.")


for device in get_devices():
    reset_keyboard(device)

# reset_keyboard("10.2.16.149:5555")
