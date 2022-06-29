# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/10 17:53
# Desc:  上报机器人状态

import requests

base_url = "https://call-on-duty-test.syriusdroids.com"
add_url = "/api/site/PwQnQb69/applet/reportStatus"  # 包含了场地的UUID链接
data = {
    "robot_uuid": "",
    "is_ldle": True,
    "current_location": "Standby_001"
}
res = requests.request("POST", url=base_url + add_url, json=data)
print(res.status_code)
