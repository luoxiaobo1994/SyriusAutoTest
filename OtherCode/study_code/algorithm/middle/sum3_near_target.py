# -*- coding:utf-8 -*-
# Author: LuoXiaoBo
# Time: 2022-12-14 22:32
# Desc: 从数组里取3个数，使他们的和最接近目标值。 假定这样的组合，只能找出一个。


class Solution:

    def threeSumClosest(self, nums, target):
        ret = float('inf')  # 基本是个废物设定。
        nums.sort()  # 先排序
        length = len(nums)
        for i in range(length - 2):  # 去掉左右指针
            left = i + 1  # 1开始
            right = length - 1  # 最后一个
            while left < right:  # 左右指针不交叉的时候
                tmp = nums[i] + nums[left] + nums[right]  # 取到的三数之和
                # 下面这里：三数之和与目标值的差值 与 无穷大与目标值的差值。 肯定是三数之和更小(更接近目标值)。只是为了刷新中间变量。
                ret = tmp if abs(tmp - target) < abs(ret - target) else ret  # 三数之和与目标值的差值关系。
                if tmp == target:  # 三数之和直接等于目标值，符合题设的唯一解。
                    return target  # 直接返回。
                if tmp > target:  # 和比目标值大
                    right -= 1  # 右边大的指针减小。
                else:
                    left += 1
        return ret
