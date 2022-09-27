# -*- coding:utf-8 -*-
# Author:LuoXiaoBo
# Time:2022-09-27 23:20

import yaml

def read_yaml(file, key=None):
    with open(file, encoding='utf-8') as f:
        value = yaml.load(stream=f, Loader=yaml.FullLoader)
        if key:
            return value[key] if value[key] else f'No value: {key}'
        return value


def write_yaml(file, data=None, mode='a'):
    if file and isinstance(data, dict):
        with open(file, encoding='utf-8', mode=mode) as f:
            yaml.dump(data, stream=f, allow_unicode=True)
    else:
        print(f"请检查输入文件路径或存入的数据类型是否是键值对。")


def clear_yaml(file):
    with open(file, encoding='utf-8', mode='w') as f:
        f.truncate()  # 清空，好像数据库清空表也是这个命令。


def update_yaml(file, data, mode='w'):
    # 暂时没有好的办法能直接改指定的键值对，全读出来，再写进去，可能是最好的办法。
    value = read_yaml(file)  # 读出来
    # print(data)
    for k, v in data.items():
        value[k] = v
    write_yaml(file, data=value, mode=mode)  # 再写进去。