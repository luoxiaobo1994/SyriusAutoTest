# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/8/19 11:14
# Desc: 判断一个字符串是否在另一个字符串里。在就返回开始的下标，不在就返回-1。

"""
内置方法：str.find()即可完成。
"""


class Solution():
    def strStr(self, h, n):
        return -1 if n not in h else h.index(n)

    def strStr2(self, h, n):
        return h.find(n)
