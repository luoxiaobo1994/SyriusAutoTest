# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/22 11:21

import requests

base_url = "https://call-on-duty-test.syriusdroids.com/api/sites"

res = requests.get(url=base_url)
print(res.text)
