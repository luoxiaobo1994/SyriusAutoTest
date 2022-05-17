# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/12 11:45
# Desc: 将csv文件中的数据,转换到json文件中.

import json
import random

file = r"./test.txt"
# x = csv.reader(file)
with open(file, 'r') as f:
    lines = f.readlines()
dic = {}
for i in lines[0].split(','):
    i = i.replace('"','')
    x,y = i.split(":")
    # print(x,y)
    dic[x] = y
# print(dic)
ptoj = json.dumps(dic)
# print(type(ptoj))
print(ptoj)

