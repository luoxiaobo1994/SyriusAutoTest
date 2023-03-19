# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/3/18 16:23
# Desc:


"""
快速排序的基本思想是在待排序的 n 个元素中任取一个元素（通常取第一个元素）作为基准，
把该元素放人最终位置后，整个数据序列被基准分割成两个子序列，所有小于基准的元素放置在前子序列中，
所有大于基准的元素放置在后子序列中，并把基准排在这两个子序列的中间，这个过程称为划分。
然后对两个子序列分别重复上述过程，直到每个子序列内只有一个元素或空为止。
这是一种二分法思想，每次将整个无序序列一分为二。归位一个元素，对两个子序列采用同样的方式进行排序，
直到子序列的长度为1或0为止。（摘自算法分析与设计第二版 有删改）

复杂度方面：
时间复杂度最好情况O(nlog2n),
时间复杂度最坏情况O(n^2),
时间复杂度平均情况O(nlog2n),
空间复杂度最好情况O(log2n),

稳定性方面： 不稳定 -->  选取中值后，中值前后的值，可能出现和中值一样的情况，无法确定分在前面。还是后面。
"""

def quick_sort(num_list):
    if len(num_list) <= 1:
        return num_list
    mid_num = num_list[len(num_list)//2]  # 中间值为轴。
    left = [num for num in num_list if num < mid_num]  # 导致不稳定
    right = [num for num in num_list if num > mid_num]  # 导致不稳定
    return quick_sort(left) + [mid_num] + quick_sort(right)

ls1 = [1,5,7,3,4,6,8,4,2,1,6,4,8,4,2,1,4,6,3,8,9,6,4,3,1,8]  # 分块会把一些数字分丢。
ls2 = [9,7,3,1,6,8,5,4,2]
print(quick_sort(ls1))
print(quick_sort(ls2))