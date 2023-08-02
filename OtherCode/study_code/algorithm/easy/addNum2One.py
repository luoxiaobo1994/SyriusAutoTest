# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/12/15 15:05
# Desc: 给定一个正整数，持续拆分各位相加，直到结果为个位数。

class Solution:

    def addDigits(self, num):
        # 什么逻辑？
        return (num - 1) % 9 + 1 if num else num


print(Solution().addDigits(123))