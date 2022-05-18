#!/usr/bin/python3

# import os
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


if __name__ == '__main__':
    s = read_more_yaml('../config/more_user.yaml')
    # for i in s:
    print(s)
