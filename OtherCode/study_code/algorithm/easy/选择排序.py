# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/7/18 17:31
# Desc:


def selectionSort(ls):
    n = len(ls)
    for i in range(n - 1):
        min = i
        for j in range(i + 1, n):
            if ls[j] < ls[min]:
                min = j
        ls[i], ls[min] = ls[min], ls[i]

a = [8,5,6,4,3,7,10,2]
selectionSort(a)
print(a)
