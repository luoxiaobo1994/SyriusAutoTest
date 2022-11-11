# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/10 9:58
# Desc: 调试的

import json

import requests


def get_data():
    data = {
        "msg_type": "text",
        "content": {
            "text": "调试"
        }
    }
    return json.dumps(data, ensure_ascii=True).encode("utf-8")


def req(data):
    # webhook
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/f27cb489-5c80-45b5-afc5-0446fe289cce"
    header = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    requests.post(url, data=data, headers=header)


if __name__ == '__main__':
    req(get_data())
