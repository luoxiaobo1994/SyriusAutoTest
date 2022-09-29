# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/9 15:46
# Desc: 画出近5个版本的DI值

from matplotlib import pyplot as plt

from base.common import read_yaml

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题

data = read_yaml('DI_GoGoReady.yaml')


def plt_DI():
    x = list(data.keys())[-5:]
    y = []
    bug = list(data.values())[-5:]  # 先获取到最新5个版本的BUG分布情况
    for i in bug:
        y.append(i['P0'] * 10 + i['P1'] * 3 + i['P2'] * 1 + i['P3'] * 0.1)
    print(y)
    plt.plot(x, y, marker='o', label='DI值')
    plt.xlabel("GoGoReady版本")
    plt.ylabel("DI值")
    plt.title("近5个GoGoReady版本DI值变化曲线")
    for a, b in zip(x, y):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=15)
    plt.legend()
    plt.show()


# print(data.keys())
plt_DI()
