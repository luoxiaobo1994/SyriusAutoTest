# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/9 11:21
# Desc: 类中new和init的区别


class User:

    def __new__(cls, *args, **kwargs):
        # new 会在init之前调用
        # 这个函数，必须return一个对象，否则实例化的对象无法正常调用实例函数。init走不下去
        # new是用来控制对象的生成过程，在对象生成之前。
        print('调用了类的__new__方法。')
        return super().__new__(cls)  # 必要的返回

    def __init__(self):
        # init是用来完善对象的
        print('调用了类的__init__方法。')

    def ppp(self):
        print('p方法')


if __name__ == '__main__':
    u1 = User()
    u1.ppp()
