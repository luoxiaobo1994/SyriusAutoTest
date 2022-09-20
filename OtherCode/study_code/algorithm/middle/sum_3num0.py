# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/16 11:31
# Desc:  从整数数组中抽取3个数,这三个数各只能取一次,期望他们结果等于0.以列表形式,返回这三个数.

# 不能完全通过,指针移动应该有问题.
class Solution:
    def threeSum(self, nums):
        res = []
        n = len(nums)
        nums.sort()  # 先排序。
        for left in range(n - 2):
            if nums[left] > 0:  # 拿到的左边的值已经大于0，和右边的组合起来，和一定大于0
                break
            right = n - 1
            if nums[left] + nums[right] < 0:  # 两边的和已经小于0，再加上中间值，也不会大于0.
                continue
            while left < right:
                target = 0 - nums[left] - nums[right]
                if target in nums[left + 1:right]:
                    r1 = [nums[left], target, nums[right]]
                    if r1 not in res:
                        res.append(r1)
                right -= 1
        return res


# 方法2
class Solution2:
    def threeSum(self, nums):
        n = len(nums)
        res = []
        if not nums or n < 3 or (len(set(nums)) == 1 and nums[0] != 0):  # 空列表，或者长度不足，或相同数值且数值不为0的。
            return res
        nums.sort()  # 排序
        for i in range(n):  # 循环遍历。
            if nums[i] > 0:  # 拿到的数值已经大于0，和后面的加和肯定就大于0了。
                break
            if (i > 0 and nums[i] == nums[i - 1]):  # 连续两个值相同。
                continue  # 跳过？
            l = i + 1  # 左指针
            r = n - 1  # 右指针
            while l < r:
                if (nums[i] + nums[l] + nums[r] == 0):
                    res.append([nums[i], nums[l], nums[r]])
                    while (l < r and nums[l] == nums[l + 1]):
                        l = l + 1
                    while (l < r and nums[r] == nums[l + 1]):
                        r = r + 1
                    l = l + 1
                    r = r + 1
                elif (nums[i] + nums[l] + nums[r] > 0):
                    r = r - 1
                else:
                    l = l + 1
            return res


ls = [-1, 0, 1, 2, -1, -4, -2, -3, 3, 0, 4]

print(Solution().threeSum(ls))
