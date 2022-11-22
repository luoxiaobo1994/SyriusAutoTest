# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/21 13:37
# Desc: 类属性和实例属性，以及调用顺序。

"""
实例查找的顺序：
1.先找类的init里面有没有。
2.再找类里面有没有单独定义。
"""


class A:
    name = 'A的类属性name'
    age = 'A的类属性age'
    xx = 'A的私有属性xx'

    def __init__(self):
        self.name = 'A的实例属性name'
        self.money = 0


class B(A):
    def __init__(self):
        self.name = 'B的实例属性name'
        super().__init__()  # 让B类拥有A类__init__内的属性。


class C:

    def __init__(self, day):
        # 私有属性，实例不能直接调用。 也不能继承给子类。
        self.__day = day  # 可以通过：c._C__day拿到。--> 私有属性的本质：python解释器将私有属性重命名了。
        # 私有属性安全吗？
        """
            相对安全，只是告诉开发者，这个属性是私有属性而已。
        """


a = A()
print(a.name)
# print(A.xx)
print(A().money)
b = B()
print(b.age)
print(b.name)
print(b.money)
print(B().money)
print(B.__mro__)

c = C(2022)
print(c._C__day)
