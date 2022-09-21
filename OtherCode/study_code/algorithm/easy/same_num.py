# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/21 9:54
# Desc:

def same_num(ls):
    for i in zip(*ls):
        print(i)


ls = [[1, 2, 3, 9, 5], [1, 2, 3, 5, 6], [1, 2, 4, 6], [1, 2, 7, 5]]

same_num(ls)
