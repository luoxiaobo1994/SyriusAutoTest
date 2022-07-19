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
    return 0


def format_data(data):
    xx = {'code': 200,
          'body': '{"version":"2.0.0.0","extensions":{},"id":"20220719132249154bgdslh8I0ycpSGHerPCRoVQfvn6jmqKkzN4waxOYTF2AD","createAt":1658208172756,"lastUpdateAt":1658209501090,"status":"FAILED","orderExecutingTime":1658209159255,"attributes":{"extensibleAttr01":"222","containerSlotIndex":0,"storageSerialNo":["6A_con-@1"]},"batchId":"20220719132249633HCGo9DwsE1fp864lbyzaLiU35","executeMessage":"storage type does not match;\\r\\nother errors:好了，没什么异常，瞎报的。\\n;\\r\\n","type":"ORDER_PICKING","priority":1,"timestamp":1658208197800,"expectedExecutionTime":1658208197800,"expectedFinishTime":1658208197800,"warehouseId":"202","notifyUrl":"https://peach-sqa-test.flexgalaxy.com/peach/notify","storages":[{"type":"6A_container"}],"items":[{"id":"item_ead827b76b2d4a15b0a595178cf12baa","name":"接口订单:退出SP 重启能否正常加载进入M5","barcode":"78zC2B64t98lO9050351","quantity":9,"imageUrl":"file:///../sdcard/syrius_guanxi_productImg/4923743543567.jpg","loadedQuantity":0,"status":"FAILED","binLocations":["A07010104"],"attributes":{"orderCode":"202_WAREHOUSE_20220719132249154bgdslh8I0ycpSGHerPCRoVQfvn6jmqKkzN4waxOYTF2AD","extensibleAttr0001":"222"}}],"droidId":"d25dfe89df2338dc3cb962fa537bf8c9"}'}
    if data:
        order_result = data['status']


if __name__ == '__main__':
    # print(get_token())
    print(findOrderById('20220719132249154bgdslh8I0ycpSGHerPCRoVQfvn6jmqKkzN4waxOYTF2AD'))
