# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/7/3 22:45
# Desc: 多接口测试时，解决登录或token依赖问题


import pytest
import requests
import datetime
import json


@pytest.fixture
def sqa_token():
    def get_token():
        base_url = 'https://flagship-sqa-test.flexgalaxy.com'
        """ 获取下单鉴权的token """
        url = base_url + '/authenication/expansion/tenant'
        data = {
            "authFlow": "AK_SK_AUTH_FLOW",
            "attributes": {
                "clientKey": "4otid7tu3lfu05p118ia7hvknq",  # 一定要找ops要
                "clientSecret": "1ac4pmokjnuu4kc8rjq5ajcm6bcol1jls2n3cnqh84ssknqvulgi"  # 一定要找ops要
            }
        }
        res = requests.post(url=url, json=data)
        print(today)
        today_token = {today: res.json()['accessToken']}  # 记录今日的token
        print(today_token)
        with open('token_of_today.json', 'w') as f:
            json.dump(today_token, f)

    today = datetime.date.today().strftime("%Y/%m/%d")
    try:
        with open('token_of_today.json', 'r') as f:
            data = json.load(f)
            if today in data:
                print(f"{today}已经获取了token,无需重复获取。请直接读取文件{'token_of_today.json'}使用。")
            else:
                get_token()
    except:
        get_token()


token()
