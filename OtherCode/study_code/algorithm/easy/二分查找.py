# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/1/3 15:07
# Desc: 二分查找法


class Solution:
    def search(self, nums, target):
        left, right = 0, len(nums - 1)
        while left < right:
            middle = left + (right - left) // 2  # 中间的下标

            if nums[middle] > target:
                right = middle - 1  # 中间的这个数大于目标值，说明目标值在左边。
            elif nums[middle] < target:
                left = middle + 1  # 相反的情况，则是在右边，刷新左指针
            else:
                return middle  # 相等的情况，则可以直接返回目标值的下标了。
        return -1  # 一直没有结果，就返回-1
