# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

from threading import Thread
from time import sleep


class a():

    def a_a(self):
        while True:
            print('.')
            sleep(1)

    def a_b(self):
        while True:
            print('..')
            sleep(0.5)


a1 = a()
tha = Thread(target=a1.a_a)
thb = Thread(target=a1.a_b)
tha.start()
thb.start()
