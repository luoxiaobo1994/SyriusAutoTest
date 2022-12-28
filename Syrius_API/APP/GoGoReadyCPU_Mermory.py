# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/12/19 10:28
# Desc: 通过adb数据，监测GoGoReady CPU和内存占用情况。

import os
import time
import csv
import re
from threading import Thread
from base.common import pp


def debug():
    adb = 'adb shell dumpsys meminfo com.syriusrobotics.platform.launcher'
    result = os.popen(adb).read()
    # 以','进行分割
    temp = ','.join(result.split())
    # 获取native值
    native = temp.split('Native,Heap')[1].split(',')[1]
    # 获取dalvik值
    dalvik = temp.split('Dalvik,Heap')[1].split(',')[1]
    # 获取total值
    total = temp.split('TOTAL')[1].split(',')[1]
    # print(native, dalvik, total)


def memoryinfo(app='com.syriusrobotics.platform.launcher'):
    alldata = [("native", "dalvik", "TOTAL")]
    # 设置循环次数
    while True:
        try:
            lines = os.popen(f"adb shell dumpsys meminfo {app}")  # adb 查看app内存
            result = lines.read()
            temp = ','.join(result.split())
            # native_heap = temp.split('Native,Heap')[1].split(',')[1]
            # print("native_heap:" + str(int(native_heap) / 1024) + 'M')
            # dalvik_heap = temp.split('Dalvik,Heap')[1].split(',')[1]
            # print("dalvik_heap:" + str(int(dalvik_heap) / 1024) + 'M')
            total = temp.split('TOTAL')[1].split(',')[1]  # 总的内存占用。
            num = int(total) / 1024
            with open('memory.txt','a') as f:
                f.write(f"{num}\n")
            pp(f"内存占用:{num:.2f}M")
            time.sleep(30)  # 等待时间
            # alldata.append([native_heap, dalvik_heap, total])
            # csvfile = open('memoryinfo.csv', 'w', encoding='utf8', newline='')
            # writer = csv.writer(csvfile)
            # writer.writerows(alldata)
            # csvfile.close()
        except IndexError:
            pp(f"内存数据获取异常，跳过本次抓取。", 'r')


def cpuinfo(count=10, app='com.syriusrobotics.platform.launcher'):
    while True:
        try:
            lines = os.popen(f"adb shell dumpsys cpuinfo {app}")
            result = lines.read()
            percent = re.findall(r'(\d+[.][0-9]*|\d+)% TOTAL', result)[0]  # 能拿到具体占用。
            time.sleep(30)
            with open('cpu.txt','a') as f:
                f.write(f"{percent}\n")
            pp(f"CPU占用:{percent}%")
        except IndexError:
            pp(f"CPU数据获取异常，跳过本次抓取。", 'r')


if __name__ == '__main__':
    t1 = Thread(target=memoryinfo)
    t2 = Thread(target=cpuinfo)

    t1.start()
    t2.start()
