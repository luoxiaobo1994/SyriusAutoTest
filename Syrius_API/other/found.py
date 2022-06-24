# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/24 15:50
# Desc:

import json

import requests
from prettytable import PrettyTable

fundlist = ['012414', '007301', '014143', '005940']
headers = {
    'content-type': 'application/json',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


def GetFundJsonInfo(fundcode):
    url = "http://fundgz.1234567.com.cn/js/" + fundcode + ".js"
    response = requests.get(url, headers=headers)
    fundDataInfo = response.text.split('({')[1]
    fundDataInfo = '{' + fundDataInfo.split('})')[0] + '}'
    fundDataInfo = json.loads(fundDataInfo)
    return fundDataInfo


# os.system("cls")
def main():
    table = PrettyTable(["名称", "昨日净值", "实时估值", "增长率"])
    for fund in fundlist:
        myfund = GetFundJsonInfo(fund)
        table.add_row([myfund['name'], myfund['dwjz'], myfund['gsz'], myfund['gszzl']])
    print(table)
    # time.sleep(5)
    # os.system("cls")


if __name__ == '__main__':
    main()
