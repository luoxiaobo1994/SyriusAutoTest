# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/15 16:53
# Desc: 给两个数组，找出他们合并之后的中位数。

class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        nums = nums1 + nums2  # 合并数组
        # 1.先排序
        nums.sort()
        # 2.取中值：长度为奇数则就是中间值，偶数则为中间两数平均。
        lenth = len(nums)
        if lenth == 1:
            return nums[0]
        if lenth % 2 == 1:
            return nums[lenth // 2]  # 奇数长度对2整除，得到的索引一定是中间值。
        else:
            return (nums[lenth // 2] + nums[lenth // 2 - 1]) / 2


print(Solution().findMedianSortedArrays([1, 3], [2]))
