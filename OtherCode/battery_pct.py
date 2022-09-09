# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/8 21:27
# Desc: 雷龙机器人充电数据处理

import re

file = r"C:\Users\luoxiaobo\batt.txt"


with open(file) as f:
    content = f.readlines()

text = ''.join(content)
# print(text)
voltage = re.findall('voltage\(V\): (\d+\.\d+)',text)
current =  re.findall('current\(A\): (\d+\.\d+)',text)
percent =  re.findall('state_of_charge_pct: (\d{1,3})',text)
print(voltage,current,percent)
