# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/18 13:08
# Desc: 测试notify
import time

import requests
from base.common import *

base_url = 'https://flagship-sqa-test.flexgalaxy.com'


def get_token():
    url = base_url + '/authenication/expansion/tenant'
    data = {
        "authFlow": "AK_SK_AUTH_FLOW",
        "attributes": {
            "clientKey": "4otid7tu3lfu05p118ia7hvknq",
            "clientSecret": "1ac4pmokjnuu4kc8rjq5ajcm6bcol1jls2n3cnqh84ssknqvulgi"
        }
    }
    res = requests.post(url=url, json=data)
    return res.json()


def send_order():
    url = 'https://flagship-sqa-test.flexgalaxy.com/order/warehouse-order/'
    headers = {
        "Authorization": 'Bearer ' + get_token()['accessToken'],
        "Content-Type": "application/json"
    }
    # print(headers)
    order_data = [{
        "id": "6A01115",
        "batchId": 123,
        "type": "ORDER_PICKING",
        "priority": 0,
        "notifyUrl": "https://peach-sqa-test.flexgalaxy.com/peach/notify",
        "timestamp": 1652853753,
        "expectedExecutionTime": 1652853753,
        "expectedFinishTime": 1652853753,
        "warehouseId": "202",
        "storages": [
            {
                "type": "6A_container"
            }
        ],
        "items": [
            {
                "name": "测试notify接口发的订单1",
                "barcode": "123456789012",
                "quantity": 2,
                "binLocations": ["A07010101"],
                "imageUrl": "",
                "attributes": {
                    "extensibleAttr0001": "222"
                }
            }
        ],
        "attributes": {
            "extensibleAttr01": "222"
        }
    }]
    res = requests.post(url, json=order_data, headers=headers)
    print(f"url:{url}\nheaders:{headers}\nbody:{order_data}")
    print('*'*50)
    print(res.json())


# print(get_token())
send_order()
