# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/21 16:31
# Desc: super学习

class A:

    def __init__(self):
        print('A')


class B(A):
    pass
    # def __init__(self):
    #     print('B')
    #     # super(B, self).__init__() # python2的写法。
    #     super().__init__()


if __name__ == '__main__':
    b = B()
