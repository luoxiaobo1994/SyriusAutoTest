# -*- coding:utf-8 -*-
# Author: LuoXiaoBo
# Time: 2022-11-21 23:35
# Desc: 集合

s = set('abcde')  # 传入一个序列，即可变为一个：无序，不重复的集合。
s.add('f')  # 可以继续加东西

i = frozenset('abcdef')
# i.add('x')  # frozenset是不可变集合，和普通集合的差异就是，不可变的。所以没有增删。


print(s)
print(i)  # 每次打印的结果顺序是不一样的。
