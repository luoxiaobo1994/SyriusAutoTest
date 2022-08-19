# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/8/19 10:56
# Desc: 读取字符串中的数值，转换为整数，直到读取非数值字符串为止。整数需要带正负。

"""
实例：
'    42' --> 42
'  -42 yes' --> -42
"""


class Solution():
    def myAtoi(self, s):
        s = s.strip()
        if not s:
            return 0
        flag = -1 if s[0] == '-' else 1
        if s[0] in ['-', '+']:
            s = s[1:]
        num = 0
        for i in s:
            if i.isdigit():
                num *= 10  # 多一位，*10倍
                num += ord(i) - 48
            else:
                break
        return max(-2 ** 31, min(flag * num, 2 ** 31 - 1))


s1 = '    -42 yes'
s2 = 'dasd'
s3 = '   '
s4 = 'aa4566'
s5 = '+1234586aaa'
print(Solution().myAtoi(s1))
print(Solution().myAtoi(s2))
print(Solution().myAtoi(s3))
print(Solution().myAtoi(s4))
print(Solution().myAtoi(s5))
