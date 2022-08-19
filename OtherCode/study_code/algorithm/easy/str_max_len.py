# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/15 13:36
# Desc: 寻找字符串的最长子串


class Solution():

    def lenthOfLongestSubstring(self, s):
        """
        :type s:str
        :rtypr: int
        """
        lenth1 = len(s)
        dic1 = {}
        maxlen = 0
        arr = list(s)
        st = ''
        for i in range(lenth1):  # 遍历整个字符串长度.
            if i == 0:  # 字符串长度为1
                st = arr[i]
            if i > 0:
                stlen = len(st)  #
                for j in range(stlen):
                    if (st[j] == arr[i]):
                        if stlen > maxlen:
                            maxlen = stlen
                        st = ''
                        break
                    else:
                        pass
                st = st + arr[i]
        countlis = [x for x in dic1.values()]
        return maxlen


print(Solution().lenthOfLongestSubstring('abcabcbb'))
