# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/3/9 23:07
# Desc: 给你两个按 非递减顺序 排列的整数数组 nums1 和 nums2，另有两个整数 m 和 n ，分别表示 nums1 和 nums2 中的元素数目。

class Solution:

    def merge(self, num1, m, num2, n):
        p1, p2 = m - 1, n - 1  # 两个指针
        tail = m + n - 1  # 合计长度
        while p1 >= 0 or p2 >= 0:
            if p1 == -1:
                num1[tail] = num2[p2]
                p2 -= 1
            elif p2 == -1:
                num1[tail] = num1[p1]
                p1 -= 1
            elif num1[p1] > num2[p2]:
                num1[tail] = num1[p1]
                p1 -= 1
            else:
                num1[tail] = num2[p2]
                p2 -= 1
            tail -= 1
