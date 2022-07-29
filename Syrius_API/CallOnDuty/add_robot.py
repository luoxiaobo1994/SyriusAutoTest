# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/22 11:24

import requests

from call_cfg import cfg

base_url = cfg()['url']  # 这是测试环境的，注意切换。
add_url = f"/api/site/Def2ixiR/portal/addRobots"  # 包含了场地的UUID链接

robot_uuids = {
    "robot_uuids": [
        # "f778cc29537a321e9d623fa7f5c36cba",  # 需要添加的机器人ID
        # "e7f222bb229fdaaad0028f2ec6c9c344",
        # "dee37aec600d37b89d8333016353a105",
        # "2aafe0dfc34f3002bce4f8ec34f333ff"
        # "ee015dec7ba43fb9bac9d46a0d0a7d3e"
        # "14d4b4ab96213fe994039bfd8306e1e1",
        # "8cdde7fe317639fb9b0ec78eebcaa3b4",
        # "ab4ee194d3443577b73abfee115bc9dd",
        # "08fba44d3e703788b5642c140b075a9b",
        # "3b2a6326b9e7386fb2e0c5fec31b03e1",
        "5e43f79646124615a1da7a821007a686",
        "bbe9859d173087b0f25e2499c50e8759",
        # "3b84f5ab260cc7353587df64c8aa8c5e"
    ]
}

res = requests.request("POST", url=base_url + add_url, json=robot_uuids)
print(res.status_code)
# print(json.dumps(res))
