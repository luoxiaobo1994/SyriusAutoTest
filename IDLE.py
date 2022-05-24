# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

from utils.file_reader import YamlReader

file = 'config/yaml_demo.yaml'

data = YamlReader(file).data
print(data)