# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/12/10 9:47

from appium import webdriver

from base.base_page import TestKey


class GGR():
    def __init__(self):
        pass

    def browser(self, devices='xxx', port='4723', platformversion='8'):
        app_data = {
            "platformName": "Android",  # 平台
            "udid": devices,
            "platformVersion": platformversion,  # 注意调试平板的安卓版本
            "deviceName": 'c5',  # 注意调试平板的IP,参数化来控制多设备。
            "apppackage": "com.syriusrobotics.platform.launcher",  # 包名
            "appActivity": "com.syriusrobotics.platform.launcher/com.syriusrobotics.platform.jarvis.MainFlutterActivity",
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
