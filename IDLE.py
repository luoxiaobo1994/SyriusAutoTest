# -*- coding: utf-8 -*-
# Author: LuoXiaoBo
# 2023/4/24 19:39
# Describe: 本地调试脚本

from base.common import *
from collections.abc import Iterable

from itertools import product, combinations

def generate_combinations(chars, length):
    # 重复排列
    repeated_perms = product(chars, repeat=length)
    for perm in repeated_perms:
        yield ''.join(perm)

    # 组合
    combs = combinations(chars, length)
    for comb in combs:
        yield ''.join(comb)


for i in generate_combinations('abc1',2):
    print(i)