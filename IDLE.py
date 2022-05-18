# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

from utils.log import Logger
from base.common import get_devices

x = get_devices()[0]
print(x)
logger = Logger().get_logger(file=f"{x}.txt")
logger.info("111")