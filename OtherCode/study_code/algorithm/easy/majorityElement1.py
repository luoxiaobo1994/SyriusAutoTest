# -*- coding:utf-8 -*-
# Author:LuoXiaoBo
# Time:2022-10-12 0:22

"""
题目明确说明：必定存在符合多数原则的数。多数原则：占比大于一半。
解题思路：
1.既然你至少占了一半的名额。那么使用对冲原理，你一个名额干掉一个其他数值，干到最后，你肯定至少剩1个。
一一对冲干掉，最后剩下的肯定是多数的那个数值了。
因此，逐一选数，每次选数，都给这个数记上一票，如果和前一次的数一样，票数+1。
如果不一样，票数-1。

"""


class Solution:
    def majorityElement(self, nums):
        major = 0
        count = 0

        for n in nums:
            if count == 0:
                major = n
            if n == major:
                count += 1
            else:
                count -= 1
        return major


ls = [2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 3, 3, 3]
print(Solution().majorityElement(ls))
