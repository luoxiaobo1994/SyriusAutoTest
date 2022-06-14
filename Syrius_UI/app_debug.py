# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/14 16:24
# Desc:

import time
from appium import webdriver

app_data = {
    "platformName": "Android",  # 平台
    "udid": 'FCQNU20A14100683',
    "platformVersion": '8',  # 注意调试平板的安卓版本
    "deviceName": 'c5',  # 注意调试平板的IP,参数化来控制多设备。
    "apppackage": 'com.android.settings',  # 包名
    "appActivity": 'com.android.settings startActivity',
    "noReset": True,  # 不要重置
    "unicodeKeyboard": True,  # 不会吊起键盘。
    # "resetKeyboard": True,  # 恢复键盘
    'newCommandTimeout': 30000,  # 命令超时时间。给长一点
    'automationName': 'UiAutomator2'  # 可能是这里导致的常断开
}

driver = webdriver.Remote('http://127.0.0.1:4730/wd/hub', app_data)
driver.implicitly_wait(10)
while True:
    print('进入显示设置界面')
    driver.start_activity('com.android.settings', '.Settings$DisplaySettingsActivity')
    time.sleep(5)
    print('进入无线设置界面')
    driver.start_activity('com.android.settings', '.Settings$WirelessSettingsActivity')
    time.sleep(5)
    print('进入系统设置界面')
    driver.start_activity('com.android.settings', '.Settings$HwSystemDashboardActivity')
    time.sleep(5)
