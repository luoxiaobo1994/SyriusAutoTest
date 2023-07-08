# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/7/8 15:02
# Desc:

class Student:

    def __init__(self, name, age, money=10):
        self.__name = name  # 私有属性，实例不能直接调用，stu1.__name 是报错的。
        self.__age = age  # 私有属性，可以实例调类再调私有属性。 stu1._Student__age
        self.money = money  # 实例属性，可以通过实例直接调用。如 stu1.

    def study(self, course_name):
        # 通过实例方法，调用私有属性。
        print(f"{self.__name}正在学习{course_name}")

    @property  # 通过装饰器，调用私有属性。
    def get_name(self):
        return self.__name

    @get_name.setter  # 修改私有属性
    def get_name(self, name):
        self.__name = name or "无名氏"


if __name__ == '__main__':
    stu1 = Student('罗小波', 18)
    stu1.study("python 设计")
    print(stu1.money)
    print(stu1._Student__name)  # 可以通过这样 调到类的私有属性。
    print(stu1.get_name)
    stu1.get_name = '张三'  # 修改私有属性，是直接赋值，而不是函数调用。 因为是被装饰的函数，类似于属性
    print(stu1.get_name)
