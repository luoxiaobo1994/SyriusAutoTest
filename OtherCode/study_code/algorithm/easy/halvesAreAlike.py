# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/11 15:42
# Desc: 将一个字符串对半分,检查两半含有的元音字母是否数量相同。

"""
前提：给的字符串长度一定是偶数。保证能对半切开。
思路：
    既然是两个数据进行对比，是否一致。两个数据一致的特点是：相减等于0.
    所以，尽管遍历字符串，只要遍历当前的字符，符合要求而且，属于前半部分，那么计数+1.
    属于后半部分，符合要求的，则计数-1. 此消彼长之间，只要最后的计数结果是0，那么两个的数量是一致的。
"""


class Solution:

    def halvesAreAlike(self, s):
        alpha = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
        count = 0
        half = len(s) / 2
        for index, i in enumerate(s):
            if i in alpha:
                if index < half:
                    count += 1
                else:
                    count -= 1
        return True if count == 0 else False


s = Solution()
print(s.halvesAreAlike('textbook'))
