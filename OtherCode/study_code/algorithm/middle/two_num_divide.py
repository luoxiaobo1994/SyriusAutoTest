# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/16 16:53
# Desc: 两数相除，结果取整数。

def solotion1(divide, divisor):
    if divide ^ divisor < 0:
        flag = -1
    else:
        flag = 1
    # 暴力解法，用被除数持续减去除数。
    count = 0
    while divide >= divisor:
        divide -= divisor
        count += 1
    return count * flag


print(solotion1(7, -2))
