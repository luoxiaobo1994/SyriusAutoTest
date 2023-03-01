# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/2/14 21:31
# Desc:  给定一个字符串 s ，请你找出其中不含有重复字符的 最长子串 的长度。

"""
输入: s = "abcabcbb"
输出: 3
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。


输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。

"""


class Solution:

    def longestString(self, s):
        # 第一步，先定义需要维护的变量
        res = ''  # 临时的子串

        start = 0  # 起势位置

        for end in range(len(s)):
            res = end
