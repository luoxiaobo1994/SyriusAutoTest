# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/24 23:34
# Desc:  迁移一个新的环境，用这个来同步所有第三方库。

import os

file = "D:\SoftData\Feishu\piplist.txt"
with open(file) as f:
    con = f.readlines()
for i in con:
    ku = i.split()[0]
    # print(ku)
    try:
        os.system(f"pip install {ku}")
    except Exception as e:
        print(e)