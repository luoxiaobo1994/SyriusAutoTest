# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/18 13:08
# Desc: 测试notify
import random
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


def random_item():
    item = {
        "name": f"接口下发的订单{item_code()}",
        "barcode": item_code(),
        "quantity": random.choice(range(1, 100)),
        "binLocations": [random.choice(['A07010202', 'A01010101', 'A03010203', 'A05010201'])],
        "imageUrl": "file:///../sdcard/syrius_guanxi_productImg/4922848674385.jpg",
        "attributes": {
            "extensibleAttr0001": "222"
        }
    }
    return item


def item_num(num=3):
    """ 一个订单内的商品数量 """
    n = random.choice(range(1, num + 1))
    items = []
    for i in range(n):
        items.append(random_item())
    return items


def random_id(siteid="202"):
    """ 用来生成单个的随机id数据. """
    timestamp = str(int(time.time()) * 1000 + 28800)  # *1000:秒-毫秒. +28800,8小时的时区差值(秒)
    id_num = {
        "id": random_time(),
        "batchId": random_time(),
        # "type": 'ORDER_PICKING',  # 指定类型时,把注释去掉,并去掉下面的随机选择.
        # "type": 'TOTAL_PICKING',  # 指定类型时,把注释去掉,并去掉下面的随机选择.
        "type": random.choice(['ORDER_PICKING', 'TOTAL_PICKING']),  # 随机选一个.
        "priority": 1,
        "notifyUrl": "https://peach-sqa-test.flexgalaxy.com/peach/notify",
        "timestamp": timestamp,
        "expectedExecutionTime": timestamp,
        "expectedFinishTime": timestamp,
        "warehouseId": siteid,
        "storages": [
            {
                # "type": '6A_container' # 指定类型时,把注释去掉,并去掉下面的随机选择.
                "type": random.choice(['1A_container', '3A_container', '6A_container', '9A_container'])  # 随机选一个
            }
        ],
        "items": item_num(),  # 每个订单有几个商品,由这个函数,再去生成.
        "attributes": {
            "extensibleAttr01": "222"
        }
    }

    return id_num


def id_num(num=5, siteid="202"):
    """ 用来生成多个id的任务,每个id包含的拣货信息由random_id生成 """
    n = random.choice(range(1, num + 1))
    id_nums = []
    for i in range(n):
        id_nums.append(random_id(siteid))
    return id_nums  # 直接返回列表套字典了.


def item_code(num=20):
    # 商品条码生成.现在是字母数字随机组合,1/3字母,2/3数字.
    alpha = random.sample(string.ascii_letters, num // 3)
    number = random.sample('0123456789' * (num // 10), num - num // 3)
    code = alpha + number
    random.shuffle(code)  # 直接原地打散了,没有返回值.
    return ''.join(code)


def send_order(num=5, siteid="202"):
    # 发单的主函数
    logger.debug(f"当前下发的场地ID是:{siteid},注意匹配机器人.")
    url = 'https://flagship-sqa-test.flexgalaxy.com/order/warehouse-order/'
    headers = {
        "Authorization": 'Bearer ' + get_token()['accessToken'],
        "Content-Type": "application/json"
    }
    order_data = id_num(num, siteid="202")  # 订单号数量
    res = requests.post(url, json=order_data, headers=headers)
    return res.json()


if __name__ == '__main__':
    send_order(siteid="202")
