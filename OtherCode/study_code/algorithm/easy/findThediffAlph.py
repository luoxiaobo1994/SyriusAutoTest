# -*- coding:utf-8 -*-
# Author:LuoXiaoBo
# Time:2022-10-15 16:02

"""
给定两个字符串 s 和 t ，它们只包含小写字母。
字符串 t 由字符串 s 随机重排，然后在随机位置添加一个字母。
请找出在 t 中被添加的字母。
示例1：
输入：s = "abcd", t = "abcde"
输出："e"
解释：'e' 是那个被添加的字母。
示例2：
输入：s = "", t = "y"
输出："y"

解题疑问：
1.如果有重复的，怎么处理？ 如abccd和abdccc

解题思路：
1.每一个字母，对应一个ASCII码，t字符串 = s字符串+1个字母。 所以，两者的ASCII码和，相差一个字符。
"""

class Solution:
    def findTheDifference(self, s, t):
        return chr(sum(map(ord,t))-sum(map(ord,s)))