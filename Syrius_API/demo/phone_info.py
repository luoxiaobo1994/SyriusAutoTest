# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/15 11:00
# Desc:

import requests

url = "http://tcc.taobao.com/cc/json/mobile_tel_segment.htm?tel=17503056030"
res = requests.get(url)
print(res.status_code)
print(res.text)
