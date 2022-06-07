# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

import random
import os
from utils.file_reader import YamlReader
import yaml
from Syrius_API.flagship.res_notify import send_order
from utils.log import logger
from time import sleep


def api_order(order_num=20, siteid='202'):
    try:
        res = send_order(num=order_num, siteid=siteid)
        if 'successData' in res:
            logger.info("通过接口下发拣货任务成功.")
        else:
            sleep(10)
            logger.debug("通过接口下发任务失败了,请检查一下.或者手动发单.")
    except Exception as e:
        logger.debug(f"通过接口下发订单的流程出现了一些异常,请注意检查.异常信息:{e}")
        sleep(10)


api_order()
