# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/22 11:38

import requests,json

base_url = "https://call-on-duty-test.syriusdroids.com"
site_uuid = '/api/site/PwQnQb69/portal/tasks'


res = requests.get(url=base_url+site_uuid)
print(res.text)