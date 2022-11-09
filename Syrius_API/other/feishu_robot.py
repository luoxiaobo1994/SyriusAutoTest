# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/9 19:26
# Desc: 飞书机器人，提醒打卡。

import base64
import hashlib
import hmac

import requests


class FeiShuRobot():

    def __init__(self, app_id='', app_secret='', chat_name=''):
        self.app_id = 'cli_a3e124a3d0389013'
        self.app_secret = 'Ak3KrBUZ1NFXSGFijYCInd1ivu76FIIx'
        self.chat_name = chat_name
        self.access_token = self.get_access_token()
        self.url = "https://open.feishu.cn/open-apis/bot/v2/hook/f27cb489-5c80-45b5-afc5-0446fe289cce"
        self.headers = {
            "Authorization": "Bearer {}".format(self.access_token),
            "Content-Type": "application/json"
        }

    def get_access_token(self):
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        try:
            res = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/", json=data)
            if res.status_code == 200:
                res_json = res.json()
                access_token = res_json.get("tenant_access_token")
                print(access_token)
                return access_token
        except Exception as e:
            return {"error": e}

    # 获取群列表
    def get_chat_list(self):
        params = {
            "page_size": 100,
            "page_token": ""
        }
        try:
            res = requests.get("https://open.feishu.cn/open-apis/chat/v4/list", params=params, headers=self.headers)
            if res.status_code == 200:
                res_json = res.json()
                data = res_json.get("data")
                groups = data.get("groups")
                print(f"群组：{groups}")
                for i in groups:
                    if i.get("name") == self.chat_name:
                        return i
        except Exception as e:
            return {"error": e}

    def send_msg(self, text):
        res = self.get_chat_list()
        chat_id = res.get("chat_id")

        data = {
            "chat_id": chat_id,
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
        try:
            res = requests.post("https://open.feishu.cn/open-apis/message/v4/send/", headers=self.headers, json=data)
            return res.json()
        except Exception as e:
            return {"error": e}


def gen_sign(timestamp, secret):
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')

    return sign


if __name__ == '__main__':
    fei = FeiShuRobot()
    fei.get_chat_list()
    # res = fei.send_msg("I am coming")
