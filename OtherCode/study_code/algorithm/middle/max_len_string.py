# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/15 17:06
# Desc: 最长回文子串

"""
解题思路：
"""


class Solution:
    def longestPalindrome(self, s):
        res = ''  # 最终要返回的子串，逐步维护。
        for i in range(len(s)):  # 遍历完整个文本。
            # 如果一开始就找到一个很长的回文，后面就取不到了。
            start = max(i - len(res) - 1, 0)  # 取的是维护子、串的长度来计算下标。从0开始。
            temp = s[start:i + 1]  # 拿到一个临时的子串，从最长，到最短。从start开始，反着取。
            if temp == temp[::-1]:  # 正序等于反序。abc = cba
                res = temp  # 那他就是要找的子串。
            else:
                temp = temp[1:]  # 不是回文，就往下继续截断。
                if temp == temp[::-1]:  # 截断之后是回文了。
                    res = temp
        return res
