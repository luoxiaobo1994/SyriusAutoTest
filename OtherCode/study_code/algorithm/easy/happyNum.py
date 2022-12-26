# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/12/15 13:51
# Desc: 判断一个数是不是快乐数。

"""
「快乐数」 定义为：

对于一个正整数，每一次将该数替换为它每个位置上的数字的平方和。
然后重复这个过程直到这个数变为 1，也可能是 无限循环 但始终变不到 1。
如果这个过程 结果为 1，那么这个数就是快乐数。
如果 n 是 快乐数 就返回 true ；不是，则返回 false

输入：n = 19
输出：true
解释：
12 + 92 = 82
82 + 22 = 68
62 + 82 = 100
12 + 02 + 02 = 1
"""


class Solution:

    def isHappyNum(self, n: int):
        pre = set([n])  # set函数要传入迭代对象，所以不能直接set(n)

        def check(num):
            lst = [int(va) ** 2 for va in str(num)]
            return sum(lst)  # 把结果返回

        while n != 1:
            n = check(n)  # 算出来结果，重新赋值给计算的数。
            if n in pre:  # 如果得到的结果，已经在预存的缓存集合里，说明，可以无限循环下去。
                return False  # 不是目标数值。
            pre.add(n)  # 不在缓存里，就继续找。
            # print(pre)
        return True


if __name__ == '__main__':
    n = 19
    print(Solution().isHappyNum(n))
