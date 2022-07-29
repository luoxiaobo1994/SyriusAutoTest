# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/23 9:34

import json

import requests

url = 'https://call-on-duty-test.syriusdroids.com/api/site/Def2ixiR/portal/taskDetail'

task_uuid = {'task_uuid': 'Ftb5E7Ck'}  # 必要的参数
count = 0


def more():
    global count
    res = requests.get(url, params=task_uuid)  # 这里要用params传,不能用json.
    info = dict(json.loads(res.text))  # 文本转json再转字典.
    print(f"url:{res.url}",
          f"cookie:{res.cookies}",
          f"reason:{res.reason}",
          f"text:{res.text}",
          f"status_code:{res.status_code}", sep='\n')
    # print_dict(info)
    # if res.status_code == 200:
    #     count += 1
    #     print('\r%d'%count)


# while True:
more()
