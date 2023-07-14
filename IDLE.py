# -*- coding: utf-8 -*-
# Author: LuoXiaoBo
# 2023/4/24 19:39
# Describe: 本地调试脚本


def tt(func):
    def gf(*args):
        print("in gf")
        func(*args)

    return gf


@tt
def foo(x):
    print(f"in foo",x)

foo(7)