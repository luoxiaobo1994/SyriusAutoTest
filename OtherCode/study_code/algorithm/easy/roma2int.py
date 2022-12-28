# -*- coding:utf-8 -*-
# Author: LuoXiaoBo
# Time: 2022-12-14 22:56
# Desc: 罗马字符转数值


class Solution:

    def romanToInt(self, s):
        d = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000,
             "IV": 3, "IX": 8, "XL": 30, "XC": 80, "CD": 300, "CM": 800}
        return sum(d.get(s[max(i - 1, 0):i + 1], d[n]) for i, n in enumerate(s))


print(Solution().romanToInt("MCMXCIV"))
