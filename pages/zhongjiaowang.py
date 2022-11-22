# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/11/18 15:41
# Desc: 定位标签练习

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

from base.base_page import TestKey


class zjw(TestKey):
    # 封装后的代码
    url = 'http://www.e658.cn/'

    def __init__(self):
        driver = webdriver.Chrome()
        super().__init__(driver)
        self.open_zjw(url=zjw.url)

    def open_zjw(self, url='https://www.baidu.com'):
        self.open_url(url)

    def click_hq(self):
        self.click_element((By.XPATH, '//a[@href="http://www.e658.cn/hq/"]'))


class old_zjw():
    # 未封装的代码。
    url = 'http://www.e658.cn/'

    def __init__(self):
        self.driver = webdriver.Chrome()
        time.sleep(2)  # 避免性能问题，需要强制等待。

    def open_zjw(self, url):
        self.driver.get(url)
        time.sleep(5)  # 避免性能问题，需要强制等待。

    def click_hq(self):
        self.driver.find_element(by=By.XPATH, value='//a[@href="http://www.e658.cn/hq/"]').click()


if __name__ == '__main__':
    zj = zjw()
    zj.click_hq()
