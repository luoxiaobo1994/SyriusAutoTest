# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

import json

import requests


def get_data():
    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "项目更新通知",
                    "content": [
                        [{
                            "tag": "text",
                            "text": "项目有更新: "
                        },
                            {
                                "tag": "a",
                                "text": "请查看",
                                "href": "https://www.baidu.com/"
                            },
                            {
                                "tag": "at",
                                "user_id": "123456"
                            }
                        ]
                    ]
                }
            }
        }
    }
    return json.dumps(data, ensure_ascii=True).encode("utf-8")


def req(data):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/f27cb489-5c80-45b5-afc5-0446fe289cce"
    header = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }
    res = requests.post(url, data=data, headers=header)
    print(res.status_code)


if __name__ == '__main__':
    req(get_data())
