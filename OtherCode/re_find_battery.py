# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/9 14:20
# Desc: 获取电池充电数据，并画图。

import re

from matplotlib import pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题

file = r"E:\工作\测试资料\battery.txt"


def get_data():
    with open(file) as f:
        content = f.readlines()
    return ''.join(content)


def get_info():
    data = get_data()
    volterge = re.findall(r'voltage\(V\): (\d+\.\d+)', data)
    current = re.findall(r'current\(A\): (\d+\.\d+)', data)
    percent = re.findall(r'state_of_charge_pct: (\d{1,3})', data)
    time_stamp = re.findall(r'I20220909 (.*?)\.', data)
    return volterge, current, percent, list(set(time_stamp))


def plt_volterge():
    volterge = [24.37, 24.72, 25.4, 25.82, 26.24, 26.75, 27.43, 28.04, 28.67, 29.02, 29.07]
    percent = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    time_stamp = [0, 10, 28, 47, 65, 84, 102, 120, 139, 166, 177]
    power = [332.6505, 337.428, 346.202, 353.9922, 360.0128, 367.2775, 376.8882, 385.55, 356.0814, 219.9716, 199.1295]

    plt.plot(time_stamp, volterge, marker='o', label='电压(V)')
    plt.xlabel("时间")
    plt.ylabel("电压值")
    plt.title("电压随时间变化趋势")
    for a, b in zip(time_stamp, volterge):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=15)
    plt.legend()
    plt.show()


def plt_current():
    current = [13.65, 13.65, 13.63, 13.71, 13.72, 13.73, 13.74, 13.75, 12.42, 7.58, 6.85]
    time_stamp = [0, 10, 28, 47, 65, 84, 102, 120, 139, 166, 177]
    plt.plot(time_stamp, current, marker='o', label='电流(A)')
    plt.xlabel("时间")
    plt.ylabel("电流值")
    plt.title("电流随时间变化趋势")
    for a, b in zip(time_stamp, current):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=15)
    plt.legend()
    plt.show()


def plt_percent():
    percent = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    time_stamp = [0, 10, 28, 47, 65, 84, 102, 120, 139, 166, 177]
    plt.plot(time_stamp, percent, marker='o', label='电池比例')
    plt.xlabel("时间")
    plt.ylabel("电池电量")
    plt.title("电池充电比例随时间变化趋势")
    for a, b in zip(time_stamp, percent):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=15)
    plt.legend()
    plt.show()


def plt_power():
    power = [332.6505, 337.428, 346.202, 353.9922, 360.0128, 367.2775, 376.8882, 385.55, 356.0814, 219.9716, 199.1295]
    time_stamp = [0, 10, 28, 47, 65, 84, 102, 120, 139, 166, 177]
    plt.plot(time_stamp, power, marker='o', label='功率(W)')
    plt.xlabel("时间")
    plt.ylabel("功率")
    plt.title("功率随时间变化趋势")
    for a, b in zip(time_stamp, power):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=15)
    plt.legend()
    plt.show()


def plt_power_percent():
    power = [332.6505, 337.428, 346.202, 353.9922, 360.0128, 367.2775, 376.8882, 385.55, 356.0814, 219.9716, 199.1295]
    percent = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    plt.plot(percent, power, marker='o', label='功率(W)')
    plt.xlabel("电池比例")
    plt.ylabel("功率")
    plt.title("功率随电池充电比例变化趋势")
    for a, b in zip(percent, power):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=15)
    plt.legend()
    plt.show()


plt_volterge()
plt_current()
plt_percent()
plt_power()
plt_power_percent()
