# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/9 16:29
# Desc: 元类编程

def func1(xself):
    print(xself.name)
    print('func1s print')


class BaseClass():
    def baseFunc(self):
        return 'i am baseclass func'


User = type('User', (), {'name': 'lxb', 'func1': func1})
u = User()
print(type(u))
u.func1()
print(u.name)

User1 = type('Userx', (BaseClass,), {'name': 'lxb', 'func1': func1})
u1 = User1()
u1.func1()
print(u1.baseFunc())
