# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/15 17:52
# Desc: 给定一个数组，数组内各个数组成一个圆柱坐标系，找出两个端点的数值，使这两个柱子组成的矩形面积最大。


class Solution:
    def maxArea(self, height):
        left, right = 0, len(height) - 1  # 左右指针
        area = 0  # 要返回的面积
        while left < right:  # 两个指针没有相遇的情况。
            tmp = min(height[left], height[right]) * (right - left)  # 当前组成的面积。
            if tmp > area:  # 当前的面积，大于已经存储的面积。
                area = tmp  # 刷新面积。
            # 情况1，左边的柱子高，右指针左移。
            if height[left] > height[right]:
                right -= 1
            # 情况2，左边的柱子矮，左指针右移。
            else:
                left += 1
        return area


ls = [1, 8, 6, 2, 5, 4, 8, 3, 7]
print(Solution().maxArea(ls))
