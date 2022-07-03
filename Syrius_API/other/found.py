# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/24 15:50
# Desc:

import json
import re
from multiprocessing.dummy import Pool
import requests
from utils.file_reader import YamlReader
from base.common import get_date

data = YamlReader('../../config/found_data.yaml').data  # 需要爬取的数据

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
    # fundDataInfo['income'] = money * float(fundDataInfo['gszzl']) / 100  # 收益
    # {'fundcode': '012414', 'name': '招商中证白酒指数(LOF)C', 'jzrq': '2022-06-27', 'dwjz': '1.2430',
    # 'gsz': '1.2425', 'gszzl': '-0.04', 'gztime': '2022-06-28 10:43', 'income': -4.0}
    return fundDataInfo


def get_found(code='012414', money='0'):
    global total
    url = "https://fundgz.1234567.com.cn/js/" + str(code) + ".js"
    response = requests.get(url, headers=headers)
    # print(type(response.text))
    # print(response.text)
    res = re.findall(r'jsonpgz\((.*?)\);', response.text)[0]  # 获取到字符串的字典。
    res = eval(res)  # 转化为字典。
    amplitude = 0.9 if float(res['gszzl']) > 0 else 1.1  # 跌了多跌一点，涨了少涨一点。
    income = float(res['gszzl']) * float(money) / 100 * amplitude
    total += income  # 本基金收益
    name = re.sub(r'[A-Za_z() ]', '', res['name']).replace('发起式','')
    # name = res['name']
    # 一个中文站2个显示长度，中文名称长度不一致，补的空格长度，会影响排版。
    # name = name.split()[0] + ' ' * (30 - len(name)*2)
    found_data = f"{code:{chr(12288)}<10}{name:{chr(12288)}<15}{res['gszzl']:{chr(12288)}<10}{income:{chr(12288)}<10.2f}"
    result.append(found_data)
    # print(f"这个基金的信息长度：{len(found_data)}")  # 文本长度都是没问题的：50


def wraper(args):
    get_found(*args)


def main():
    print(f"{'基金代码':{chr(12288)}<10}{'基金名称':{chr(12288)}<13}{'实时估值':{chr(12288)}<8}{'预计收益':{chr(12288)}<10}")
    p = Pool()
    p.map(wraper, dict(data).items())
    result.sort()  # 保证每次打印的顺序是一致的，避免多线程导致的顺序不一样。
    for i in result:
        if '-' in i:
            print(f"\033[1;36m{i}\033[0m")
        else:
            print(f"\033[1;31m{i}\033[0m")
    print(f"{get_date()} 预计收益：{total:.2f}元。")


if __name__ == '__main__':
    main()
    # get_found(code='014605')
    # print(dict(data).items())
    # main2()
