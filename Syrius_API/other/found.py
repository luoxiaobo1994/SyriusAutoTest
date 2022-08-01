# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/24 15:50
# Desc:

import json
import re
from multiprocessing.dummy import Pool

import requests

from base.common import get_time
from utils.file_reader import YamlReader

data = YamlReader('found_data.yaml').data  # 需要爬取的数据
space = chr(12288)
total = 0  # 当日收益
result = []  # 结果集合
headers = {
    'content-type': 'application/json',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


def GetFundJsonInfo(fundcode):
    url = "https://fundgz.1234567.com.cn/js/" + fundcode + ".js"
    response = requests.get(url, headers=headers)
    fundDataInfo = response.text.split('({')[1]
    fundDataInfo = '{' + fundDataInfo.split('})')[0] + '}'
    fundDataInfo = json.loads(fundDataInfo)
    # {'fundcode': '012414', 'name': '招商中证白酒指数(LOF)C', 'jzrq': '2022-06-27', 'dwjz': '1.2430',
    # 'gsz': '1.2425', 'gszzl': '-0.04', 'gztime': '2022-06-28 10:43'}
    return fundDataInfo


def get_found(code='012414', money='0'):
    global total
    url = "https://fundgz.1234567.com.cn/js/" + str(code) + ".js"
    response = requests.get(url, headers=headers)
    # print(response.text)
    res = re.findall(r'jsonpgz\((.*?)\);', response.text)[0]  # 获取到字符串的字典。
    res = eval(res)  # 转化为字典。
    amplitude = 0.95 if float(res['gszzl']) > 0 else 1.05  # 跌了多跌一点，涨了少涨一点。
    income = float(res['gszzl']) * float(money) / 100 * amplitude
    total += income  # 本基金收益
    name = re.sub(r'[A-Za_z() ]', '', res['name']).replace('发起式', '')
    found_data = f"{code:{space}<10}{name:{space}<15}{res['gszzl']:{space}<10}{income:{space}<10.2f}"
    result.append(found_data)


def wraper(args):
    get_found(*args)


def main():
    print(f"{'基金代码':{space}<10}{'基金名称':{space}<13}{'实时估值':{space}<8}{'预计收益':{space}<10}")
    p = Pool()
    p.map(wraper, dict(data).items())
    result.sort()  # 保证每次打印的顺序是一致的，避免多线程导致的顺序不一样。
    for i in result:
        if '-' in i:
            print(f"\033[1;36m{i}\033[0m")
        else:
            print(f"\033[1;31m{i}\033[0m")
    print(f"\n{get_time()} 预计收益：{total:.2f}元。")


if __name__ == '__main__':
    main()
