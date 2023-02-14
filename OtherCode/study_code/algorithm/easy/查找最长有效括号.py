# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/2/13 22:35
# Desc:

class Solution:

    def longestValidParentheses(self, s):
        res = 0
        stack = [-1]  # 栈
        for i, c in enumerate(s):
            if c == "(":
                stack.append(i)
            elif len(stack) == 1:
                stack.pop()
                stack.append(i)
            else:
                stack.pop()
                res = max(res, i - stack[-1])

        return res
