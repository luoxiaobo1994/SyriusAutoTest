# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/10/12 15:53
# Desc: 判断一个数是不是3的幂

class Solution:
    def isPowerOfThree(self, n):
        while n > 1:
            if n % 3 != 0:
                return False
            n = n // 3
        return n == 1
