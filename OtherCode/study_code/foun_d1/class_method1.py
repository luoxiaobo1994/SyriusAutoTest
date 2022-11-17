# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/16 10:12
# Desc: 类方法，实例方法

from base.common import *


class Demo:
    date1 = '2022'

    def __new__(cls, *args, **kwargs):
        print('执行__new__方法')
        return super().__new__(cls)

    def __init__(self, year, month, day):
        print('进入了初始化函数__init__')
        self.year = year
        self.month = month
        self.day = day

    # 实例方法
    def __str__(self):
        # 打印实例对象时，可以直接返回的字符串。
        return f"{self.year}/{self.month}/{self.day}"

    # 静态方法
    @staticmethod
    def parse_string(date):
        year, month, day = tuple(date.split('-'))
        return Demo(int(year), int(month), int(day))

    # 类方法
    @classmethod
    def print_date(cls):
        print(cls.date1)


if __name__ == '__main__':
    date = Demo(2022, 11, 16)
    print(date)
    dd()
    # 使用静态方法传参,静态方法也走了__new__,__init__两个方法，但是不需要对init传参
    new_day = Demo.parse_string('2022-11-17')
    print(new_day)
    dd()
    # 类方法，没有执行__new__,__init__。直接使用的。
    Demo.print_date()
