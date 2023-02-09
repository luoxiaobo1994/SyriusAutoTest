# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/8/4 13:46
# Desc: Flagship API

from utils.mylog import Logger

logger = Logger(file='../../tempData/flagshiplog.txt')


class Test_FlagshipAPI():

    def setup_class(self):
        logger.debug("获取Token")
