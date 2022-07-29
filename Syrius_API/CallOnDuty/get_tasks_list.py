# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/22 11:38

import requests

from call_cfg import cfg

base_url = cfg()['url']  # 这是测试环境的，注意切换。
# base_url = "https://call-on-duty-test.syriusdroids.com"
site_uuid = f'/api/site/{cfg()["site"]}/portal/tasks'

res = requests.get(url=base_url + site_uuid)
print(res.text)
