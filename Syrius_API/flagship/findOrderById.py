# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/22 11:15
# Desc: 通过ID查找订单


from base.Requests_API import requests_api
from res_notify import get_token
from utils.file_reader import YamlReader
from utils.log import logger

base_url = YamlReader('../../config/api_oreder_confiog.yaml').data['base_url']
url = '/order/warehouse-order/'

header = {'Authorization': 'Bearer ' + get_token()['accessToken']}


def findOrderById(orderid=''):
    if orderid:
        data = requests_api(method='GET', url=base_url + url + orderid, headers=header)
        if data['code'] == 200:
            return data
        else:
            logger.warning(f'查询失败，失败信息：{data}')
            return 'Find error'
    logger.warning("请输入正确的订单编号。")


if __name__ == '__main__':
    # print(get_token())
    print(findOrderById('20220621152350797Ar'))
