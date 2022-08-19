# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/15 14:28
# Desc: 双指针找最长无重复子串

class Solution:
    def lenthOfLongestSubstring(self, s):
        occ = {}
        n = len(s)
        if n == 0:
            return 0
        rk, ans, ml = 0, 0, 1
        while rk < n:  # 没有遍历完之前
            if s[rk] not in occ:  # 当前字符,没有在临时字典里
                occ[s[rk]] = rk  # 当前字符为键,下标为右指针的值
                rk += 1  # 指针往前挪.
                ml = max(ml, rk - ans)  # 最长的长度从默认和左指针与右指针差值中选.
            else:  # 当前字符,已经在临时字典里了.
                b = occ[s[rk]] + 1  # 当前字符的数量+1
                for j in range(ans, b):  # 右指针到
                    del occ[s[j]]  # 删除字典中与右指针所指向字符相同的字符（记为a）以及其前面的所有字符，同时把左指针更新为a+1
                ans = b  # 左指针刷新
            print(occ)
        return ml


print(Solution().lenthOfLongestSubstring('abcabcbb'))
