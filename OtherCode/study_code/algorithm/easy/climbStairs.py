# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/22 10:11
# Desc: 爬楼梯


# 一维dp，自底向上
def climbStairs(self, n):
    a = b = 1  # 递归终点
    for i in range(2, n + 1):
        a, b = b, a + b
    return b
