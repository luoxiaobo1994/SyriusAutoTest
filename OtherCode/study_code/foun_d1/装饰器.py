# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/7/14 21:46
# Desc: 装饰器详解


def wrap1(func):
    print(f"装饰器1：普通装饰器。")

    def inner():
        func()

    return inner


def wrap2(wrap_arg):
    print(f"装饰器2：装饰器自带参数 --> {wrap_arg}")

    def outer(func):  # 第一层嵌套，需要传入func函数名称
        def inner():
            func()  # 被装饰函数
            # 其他功能逻辑

        return inner

    return outer


def wrap3(func):
    print(f"装饰器3：被装饰函数需要带参数的情况")

    def inner(*args):
        func(*args)  # 被装饰函数需要自带参数的情况。

    return inner


def wrap4(func):
    print(f"装饰器4：被装饰函数需要返回数据的情况")

    def inner(*args):
        res = func(*args)  # 被装饰函数，有返回值的情况。
        return res

    return inner


@wrap1
def func1():
    print(f"普通函数")


@wrap2("装饰器自己的参数")
def func2():
    print("装饰器自己带了什么参数。")


@wrap3
def func3(name, age):
    print(f"被装饰函数自己带的参数：name:{name},age:{age}")


@wrap4
def func4(name):
    return name


func1()
func2()
func3('luoxiaobo', 29)
print(func4('被装饰函数要返回的数据'))
