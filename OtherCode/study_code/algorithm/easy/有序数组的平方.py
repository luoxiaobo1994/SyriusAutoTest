# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/1/3 15:34
# Desc: 给定一个数组，已排序好，有负数正数。将他们分别求平方，求得的结果升序排序。

class Solution:

    def sqrnum(self, nums):
        n = len(nums)
        i, j, k = 0, n - 1, n - 1
        ans = [-1] * n  # 结果集合
        while i <= j:
            lm = nums[i] ** 2
            rm = nums[j] ** 2
            if lm > rm:
                ans[k] = lm
                i += 1
            else:
                ans[k] = rm
                j -= 1
            k -= 1
        return ans


print(Solution().sqrnum([-7, -3, 2, 3, 11]))
