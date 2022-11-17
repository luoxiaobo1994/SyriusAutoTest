# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/16 15:50
# Desc: 有效的括号。leetcode-20

"""
1.下意识反应，双指针。
2.既然成对出现，此消彼长也能实现。 但是顺序，可能有点问题。
"""


class Solution:

    def isValid(self, s):
        dic = {'{': '}', '[': ']', '(': ')', '?': '?'}  # 存储需要的括号
        stack = ['?']  # 栈
        for c in s:  # 遍历字符串。
            if c in dic:  # 根据题目，这一步一定是存在。
                stack.append(c)  # 循环拿到的字符，丢到栈里。
            elif dic[stack.pop()] != c:  #
                return False
        return len(stack) == 1

    def isValid2(self, s):
        if len(s) % 2 != 0:
            return False
        while '()' in s or '[]' in s or '{}' in s:
            s = s.replace('[]', '').replace('()', '').replace('{}', '')
        return s == ''


s = '({}[)]({[]})'
print(Solution().isValid2(s))
