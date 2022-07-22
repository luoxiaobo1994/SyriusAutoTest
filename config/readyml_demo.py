# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/27 13:37
# Desc: 用来测试读取配置文件的脚本.

from base.common import *
from utils.file_reader import YamlReader

file = "yaml_demo.yaml"
data = YamlReader(file).data
print(f"全部数据：{data}")
print("-*" * 20)
for i in data:
    x = str(type(data[i]))
    print(f"type:{x:<23}{i}: {data[i]}")

if data['yes11']:
    print('yes11')
if data['no22']:  # 正确读取为False的.
    print('no22')

# update_yaml('site_info.yaml', {'api_order': False})
data = read_yaml('site_info.yaml')
print(data[data['SpeedPicker_cn2']])
print(get_filename())
