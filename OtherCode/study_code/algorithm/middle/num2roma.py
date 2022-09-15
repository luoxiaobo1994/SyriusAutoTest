# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/15 18:54
# Desc: 罗马数字包含以下七种字符： I， V， X， L，C，D 和 M。将阿拉伯数字转为罗马数字。

class Solution:
    def intToRoman(self, num):
        hashmap = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC',
                   50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}
        res = ''  # 返回的是一个字符串
        for key in hashmap:
            if num // key != 0:
                count = num // key
                res += hashmap[key] * count
                num %= key
        return res
