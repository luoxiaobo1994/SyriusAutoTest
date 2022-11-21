# -*- coding:utf-8 -*-
# Author: LuoXiaoBo
# Time: 2022-11-21 22:42
# Desc: 上下文管理器with主要实现原理是两个魔法方法__enter__, __exit__

class Demo():

    def __enter__(self):
        print("enter")
        # 获取资源了
        return self  # 返回了实例自身，或者你也可以自定义返回什么，但是注意结合结果一起看看。

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 参数是自动补全的
        print("exit")

    def do_somthing(self):
        print("do something")


with Demo() as demo:
    demo.do_somthing()
