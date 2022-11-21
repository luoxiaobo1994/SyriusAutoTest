# -*- coding:utf-8 -*-
# Author: LuoXiaoBo
# Time: 2022-11-21 22:20
# Desc: super真的是调用了父类的__init__吗？


# 答：并不是,super是将当前类继承的下一个类的init方法执行了一遍。
# 下一个的解释： 当前类的__mro__属性的顺序的下一个。
# 如下面这个例子，D继承于B,C， 而B继承于A。  D的继承顺序：D-B-A-C-object
# 如果只是D和D里面都有super,那么会执行一遍B的init，B里面的super再次调用，根据顺序，到了A的init，所以D的实例创建时，打印了D,B,A。
# 将上面的条件做一部分修改：B没有继承A。那么创建D的实例时，D的super会调用B的init。B的init会调用C的init，所以此时打印为：D,B,C

class A:

    def __init__(self):
        print("A")


class B(A):

    def __init__(self):
        print("B")
        super().__init__()


class C:

    def __init__(self):
        print("C")


class D(B, C):

    def __init__(self):
        print("D")
        super().__init__()


if __name__ == '__main__':
    print(D.__mro__)
    print(B.__mro__)
    d = D()
    # a = A()
