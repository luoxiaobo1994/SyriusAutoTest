# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

from utils.log2 import Logger

file = __file__.split('\\')[-1].replace('.py', '.txt')
logger = Logger(file=file).get_logger()
logger.debug(f"当前日志记录文件为：{file}")
