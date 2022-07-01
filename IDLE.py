# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

from multiprocessing.dummy import Pool

total = 0


def func(a, b):
    global total
    print(f"a:{a},b:{b}")
    total += b
    # return a + b


def wraper(args):
    func(*args)


d = {'甲': 1, '已': 2, '丙': 3}
p = Pool()
p.map(wraper, d.items())
print(total)
