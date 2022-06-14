# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/14 15:11
# Desc: APP启动参数.

from appium import webdriver
from base.base_page import TestKey


class APP():
    def __init__(self):
        pass

    def browser(self, devices='xxx', port='4723', platformversion='8', appname='', activity=''):
        app_data = {
            "platformName": "Android",  # 平台
            "udid": devices,
            "platformVersion": platformversion,  # 注意调试平板的安卓版本
            "deviceName": 'c5',  # 注意调试平板的IP,参数化来控制多设备。
            "apppackage": appname,  # 包名
            "appActivity": activity,
            "noReset": True,  # 不要重置
            "unicodeKeyboard": True,  # 不会吊起键盘。
            # "resetKeyboard": True,  # 恢复键盘
            'newCommandTimeout': 30000,  # 命令超时时间。给长一点
            'automationName': 'UiAutomator2'  # 可能是这里导致的常断开
        }
        br = webdriver.Remote(f"http://localhost:{port}/wd/hub", app_data)
        driver = TestKey(br)
        return driver


# s = GGR()
# driver = s.browser()

if __name__ == '__main__':
    d = GGR().browser(devices='10.111.150.31:5555', port=4725)
