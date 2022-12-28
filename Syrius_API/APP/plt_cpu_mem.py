# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/12/28 15:16
# Desc: 把获取到的数据，可视化。

from matplotlib import pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题


def plt_cpu():
    with open('cpu.txt') as f:
        data = f.readlines()
    data = [float(i.replace('\n', '')) for i in data]
    x = range(len(data))

    plt.plot(x, data)
    plt.xlabel('时间')
    plt.ylabel('CPU占用率%')
    plt.title('GoGoReady CPU占用率图表')
    plt.show()


def plt_mem():
    with open('memory.txt') as f:
        data = f.readlines()
    data = [float(i.replace('\n', '')) for i in data]
    x = range(len(data))

    plt.plot(x, data)
    plt.xlabel('时间')
    plt.ylabel('内存使用情况/M')
    plt.title('GoGoReady 内存使用图表')

    plt.show()


if __name__ == '__main__':
    plt_mem()
    plt_cpu()
