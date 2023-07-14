# -*- coding: utf-8 -*-
# Author: LuoXiaoBo
# 2023/7/14 10:39
# Describe: 读写文件的函数，主要是读写json和yaml。

import yaml
import json


def read_yaml(file):
    """ 读取单个文档 """
    with open(file, 'r', encoding="utf-8") as f:
        res = yaml.safe_load(f)
    return res  # 读出来是字典的.


def read_more_yaml(file):
    """ 读取多个文档 """
    data = []
    with open(file, 'r', encoding="utf-8") as f:
        res = yaml.safe_load_all(f)
        for item in res:  # 每个都是一个字典.
            data.append(item)
        # for i in res:
        #     print(i)
    return data  # 字典集合的列表.


def read_json(file, key=None):
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
    return data.get(key, 'json文件读取函数：没有这个键') if key else data


def update_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f)


if __name__ == '__main__':
    s = read_more_yaml('../config/more_user.yaml')
    # for i in s:
    print(s)
