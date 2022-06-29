# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/25 15:29
# Desc:

import requests

from utils.file_reader import YamlReader

config_data = YamlReader('../../config/api_oreder_confiog.yaml').data
base_url = config_data['base_url']


def get_token():
    url = base_url + '/authenication/expansion/tenant'
    data = config_data['authdata']
    res = requests.post(url=url, json=data)
    return res.json()


def total_picking_order():
    pass


def order_picking_order():
    pass


def putaway_order():
    pass

# print(get_token())
