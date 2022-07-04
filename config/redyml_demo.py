# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/27 13:37
# Desc: 用来测试读取配置文件的脚本.

from utils.file_reader import YamlReader

file = "yaml_demo.yaml"
data = YamlReader(file).data
for i in data:
    x = str(type(data[i]))
    print(f"type:{x:<23}{i}: {data[i]}")
