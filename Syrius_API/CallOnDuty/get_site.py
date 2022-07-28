# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/22 11:21

import requests

base_url = "https://callonduty-cn-sqa-test.syriusdroids.com"

res = requests.get(url=base_url + '/api/sites')
print(res.text)
