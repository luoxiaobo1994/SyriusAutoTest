# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/22 10:47


import json

import requests

base_url = "https://call-on-duty-test.syriusdroids.com"  # 基础网址
uuid = "/api/site/{site_uuid}/portal/tasks"  # 添加任务的api
create_site = '/api/site/create'  # 添加场地的api
params = {
    'site_name': 'CE_test'
}

res = requests.request("post", url=base_url + create_site, json=params)
print(json.dumps(res.json()))
