# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/22 10:47


import requests

# base_url = "https://call-on-duty-kr.syriusdroids.com"  # 基础网址
base_url = "https://callonduty-cn-sqa-test.syriusdroids.com"  # 基础网址
create_site = '/api/site/create'  # 添加场地的api
params = {
    'site_name': 'SQA_test'
}

res = requests.request("post", url=base_url + create_site, json=params)
print(res.json())
