# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/9 19:26
# Desc: 飞书机器人，提醒打卡。

import hashlib
import base64
import hmac
import requests


def gen_sign(timestamp, secret):
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')

    return sign


def send_msg(msg=''):
    web_hook = "https://open.feishu.cn/open-apis/bot/v2/hook/f27cb489-5c80-45b5-afc5-0446fe289cce"
    data_1 = {"msg_type":"text","content":{"text":"测试机器人"}}
    requests.post(url=web_hook,data=data_1)
    # print()

if __name__ == '__main__':
    send_msg()