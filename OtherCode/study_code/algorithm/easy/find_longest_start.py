# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/16 11:07
# Desc: 查找最长公共前缀

# 方法1,自己的解法
# 思路,从第一个元素开始取一位一位的取前缀,有一位不符合,就退出循环.
class Solution1:
    def longestCommonPrefix(self, strs):
        res = ''  # 需要回传的结果.
        # 从第一个开始取.
        for i in range(len(strs[0])):  # 根据这个长度,开始去找.
            try:
                if all(map(lambda x: x[i] == strs[0][i], strs)):  # 如果,每一个元素的相同位置的字符一致.
                    res += strs[0][i]  # 结果加上这个字符.
                else:
                    break
            except:
                break  # 因为后面的元素,可能有短的情况. 会超索引,所以要异常捕捉.
        return res


# 方法2,题解.靠zip函数.
class Solution():
    # ls = ['flower','fleet','flunce']  ==> fl
    def longestCommonPrefix(self, strs):
        res = ''
        for tmp in zip(*strs):  # 一个迭代器：[(f,f,f),(l,l,l),(o,e,u)...]
            tmp_set = set(tmp)
            if len(tmp_set) == 1:  # 全是相同的值，说明这个位大家都一样。
                res += tmp[0]  # 截取到的结果加上这个值
            else:
                break
        return res
