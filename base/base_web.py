# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021-07-12 15:49

import unittest

from selenium import webdriver

from utils.log import logger


# 网页浏览器初始化
class WebUtil(unittest.TestCase):
    """
    这里创建一个基础类,用于开启和关闭浏览器.用例部分,不需要再继承unittest.TestCase,直接继承这个基础类BaseUtil即可.

    """

    def setUp(self) -> None:
        # global driver
        self.driver = webdriver.Chrome()
        # driver = self.driver
        # self.driver = TestKey(driver)

    def tearDown(self) -> None:
        # time.sleep(2)
        self.driver.quit()
        logger.info("用例执行完成,关闭浏览器.")
