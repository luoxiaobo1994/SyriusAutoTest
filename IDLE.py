# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

import os

file = "D:\SoftData\Feishu\piplist.txt"
with open(file) as f:
    con = f.readlines()
for i in con:
    ku = i.split()[0]
    try:
        os.system(f"pip install {ku}")
    except Exception as e:
        print(e)

print('2334')
