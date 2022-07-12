# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/12 11:25
# Desc: 不定参数和关键字参数测试


def func1(a, b, *args, **kwargs):
    print(f"a:{a},b:{b},args:{args},kwargs:{kwargs}")


def func2(a, b, *args, **kwargs):
    print(f"a:{a},b:{b}")  # a:1,b:2
    print(*args)  # 3 4 5.  如果print(args) ==> (3,4,5)
    print(kwargs)  # {'x': 6}
    print(kwargs.get('x', ''))  # 6
    print(kwargs.get('y', ''))  # 无


func1(1, 2, 3, 4, 5, x=6)  # a:1,b:2,args:(3, 4, 5),kwargs:{'x': 6}
func2(1, 2, 3, 4, 5, x=6)  # 见上面实际结果。
