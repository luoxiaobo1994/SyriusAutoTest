# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/27 13:37
# Desc: 用来测试读取配置文件的脚本.

from utils.file_reader import YamlReader

file = 'speedpicker_config.yaml'

data = YamlReader(file).data

for i,v in data.items():
    print(i,v)
