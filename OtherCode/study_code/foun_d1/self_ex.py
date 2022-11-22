# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/21 14:20
# Desc: 自省机制：通过一定机制查询到对象的内部结构。

class Person:
    name = 'User'  # 子类的自省机制，也查不到父类的这个属性。

    def __init__(self):
        self.mail = 'xxx@.com'


class Student(Person):
    # name = '张三'  # 自省机制查不到这个属性。

    def __init__(self, school_name):
        self.school_name = school_name
        self.age = 18
        super().__init__()  # 超继承父类，子类的实例自省，才能看到父类的属性。


if __name__ == '__main__':
    stu = Student('深职院')
    stu.__dict__['school_addr'] = '深圳市南山区西丽街道'  # 也可以给实例新加一个属性，和stu.school_addr一样的。
    print(stu.__dict__)
    stu2 = Student('深职院22')  # 这个实例2，就没有school_addr
    stu2.school_age = 78  # 实例的私有属性，别的实例没有。
    print(stu2.__dict__)
    print(dir(stu))
    print(dir(stu2))
