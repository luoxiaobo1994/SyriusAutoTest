# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/24 15:50
# Desc:

import json
import re

import requests
from prettytable import PrettyTable

from utils.file_reader import YamlReader

data = YamlReader('../../config/found_data.yaml').data

fundlist = ['012414', '007301', '014143', '005940', '009163', '014605']
sum = 0  # 当日收益
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


# os.system("cls")
def main():
    sum = 0  # 预计收益
    table = PrettyTable(["名称", "昨日净值", "实时估值", "涨跌幅"])
    for fund in data:
        # print()
        myfund = GetFundJsonInfo(data[fund]['code'])
        table.add_row([myfund['name'], myfund['dwjz'], myfund['gsz'], myfund['gszzl']])
        sum += int(data[fund]['money']) * float((myfund['gszzl'])) / 100 * 0.9  # 这边估值偏高
    print(table)
    print(f"预计收益：{sum:.2f}元。")
    # time.sleep(5)
    # os.system("cls")


def get_found(code='009163', money='0'):
    global sum
    url = "https://fundgz.1234567.com.cn/js/" + str(code) + ".js"
    response = requests.get(url, headers=headers)
    # print(type(response.text))
    # print(response.text)
    res = re.findall(r'jsonpgz\((.*?)\);', response.text)[0]  # 获取到字符串的字典。
    res = eval(res)  # 转化为字典。
    income = float(res['gszzl']) * float(money) / 100
    sum += income
    print(f"{res['fundcode']:<10}{res['name']:^30}{res['gszzl']:^10}{income:^10.2f}")


def main2():
    print(f"{'代码':<10}{'名称':^30}{'实时估值':^10}{'预估收益':^10}")
    # print(data)
    for fund in data:
        # print(fund,fund['money'])
        # print(type(fund['money']),data[fund]['money'])
        get_found(code=fund, money=data[fund]['money'])
    print(f"预计收益：{sum:.2f}")


if __name__ == '__main__':
    # main()
    # get_found()
    # print(data)
    main2()
