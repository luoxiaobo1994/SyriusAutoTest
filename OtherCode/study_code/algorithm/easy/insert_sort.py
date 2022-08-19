# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/17 15:44
# Desc: 插入排序, 好比抽牌


def insert_sort(ls):
    for i in range(1, len(ls)):  # i 表示摸到的牌的下标.
        tmp = ls[i]
        j = i - 1  # j表示手里的牌的下标
        while j >= 0 and ls[j] > tmp:
            ls[j + 1] = ls[j]  # 交换
            j -= 1
        ls[j + 1] = tmp
        print(ls)


def insert_sort_gap(ls, gap):
    for i in range(1, len(ls)):
        tmp = ls[i]
        j = i - 1
        while j >= 0 and ls[j] > tmp:
            ls[j + 1] = ls[j]  # 交换
            j -= 1
        ls[j + 1] = tmp
        print(ls)
