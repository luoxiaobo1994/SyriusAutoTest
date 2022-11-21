# -*- coding:utf-8 -*-
# Author:LuoXiaoBo
# Time:2022-11-19 11:19
# Desc: 模仿手机的九键输入法，按下不同的数字组合，能产生什么样的字符串。

class Solution:

    def letterCombinations(self, digits: str):
        if not digits:
            return []
        phone = ['abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz']
        queue = ['']  # 初始化队列
        for digit in digits:  # 按下几个按键，循环几次。
            for _ in range(len(queue)):  # 每一次循环，都遍历完刷新的队列数据。
                tmp = queue.pop(0)  # 把队列里的第一个数据拿出来。
                for letter in phone[ord(digit) - 50]:  # 当前处理的数字按键，对应的字符。
                    queue.append(tmp + letter)  # 队列第一个数据(已经被取出，不再队列里的)，依次拼接新按键的字符。组成新字符串，刷新队列数据。
        return queue

    def letterCombinations2(self, digits: str):
        if not digits:
            return []
        # 方法2，回溯。 看着有点递归思想。
        phone = {'2': ['a', 'b', 'c'],
                 '3': ['d', 'e', 'f'],
                 '4': ['g', 'h', 'i'],
                 '5': ['j', 'k', 'l'],
                 '6': ['m', 'n', 'o'],
                 '7': ['p', 'q', 'r', 's'],
                 '8': ['t', 'u', 'v'],
                 '9': ['w', 'x', 'y', 'z']}

        def backtrack(combination, nextdight):
            if len(nextdight) == 0:
                res.append(combination)
            else:
                for letter in phone[nextdight[0]]:  #
                    backtrack(combination + letter, nextdight[1:])

        res = []
        backtrack('', digits)
        return res


s = Solution()
print(s.letterCombinations2('2345'))
