# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/22 10:47


import requests

from call_cfg import cfg

base_url = cfg()['url']  # 这是测试环境的，注意切换。
create_site = '/api/site/create'  # 添加场地的api
params = {
    'site_name': 'SQA2_test'
}

res = requests.request("post", url=base_url + create_site, json=params)
print(res.json())
