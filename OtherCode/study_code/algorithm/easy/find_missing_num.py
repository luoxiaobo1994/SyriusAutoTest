# -*- coding:utf-8 -*-
# Author:LuoXiaoBo
# Time:2022-10-12 0:44

"""
给定一个包含 [0, n] 中 n 个数的数组 nums ，找出 [0, n] 这个范围内没有出现在数组中的那个数。
nums 中的所有数字都 独一无二

自己的思路：
1.排序 --但是增加了复杂度。
2.逐个遍历查找。

解答思路：
从0开始的升序列表，就是一个等差数列，且差值是1. 那么。从0到n的等差数列的和。和现有列表的和的差值，就是那个丢失的数字。
"""


class Solution:
    def missingNumber(self, nums):
        n = len(nums)
        return n * (n + 1) // 2 - sum(nums)
