# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/14 16:24
# Desc:

import os
from time import sleep
from appium import webdriver
from pages.pad_setings_page import *
from base.common import get_android_version

os.system(f'adb push {"SyriusLogo.jpeg"} /sdcard/Pictures')
sleep(3)

app_data = {
    "platformName": "Android",  # 平台
    # "udid": 'FCQNU20A14100683',
    "platformVersion": get_android_version(device=''),  # 注意调试平板的安卓版本
    "deviceName": 'c5',  # 注意调试平板的IP,参数化来控制多设备。
    "apppackage": 'com.android.settings',  # 包名
    "appActivity": 'com.android.settings startActivity',
    "noReset": True,  # 不要重置
    "unicodeKeyboard": True,  # 不会吊起键盘。
    # "resetKeyboard": True,  # 恢复键盘
    'newCommandTimeout': 30000,  # 命令超时时间。给长一点
    'automationName': 'UiAutomator2'  # 可能是这里导致的常断开
}

driver = webdriver.Remote('http://127.0.0.1:4725/wd/hub', app_data)
driver.implicitly_wait(10)


def download_ggr():
    path = './'
    file_path = os.path.join(path, 'GoGoReady-latest-prod.apk')
    res = requests.get(url=download)
    with open(file_path, 'wb') as f:
        f.write(res.content)
    os.system(f'adb install -r {file_path}')


def adb_setting():
    os.system(
        'adb shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0')
    os.system('adb shell pm uninstall --user 0 com.huawei.vassistant')


def set_sleep(option=''):
    sleep(5)
    driver.start_activity('com.android.settings', '.Settings$DisplaySettingsActivity')
    if not option:
        driver.find_element(By.XPATH, '//android.widget.TextView[@text="休眠"]').click()
        sleep(1)
        driver.find_element(By.XPATH, '//android.widget.CheckedTextView[@text="永不"]').click()
    else:
        driver.find_element('//android.widget.TextView[@text="10 分钟"]')


def set_wallpaper():
    driver.start_activity('com.android.settings', '.Settings$DisplaySettingsActivity')
    sleep(2)
    driver.find_element(By.XPATH, '//android.widget.TextView[@text="壁纸"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//android.widget.TextView[@text="设置壁纸"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//android.view.View[@content-desc="图库"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//android.widget.TextView[@text="图片"]').click()
    sleep(1)
    driver.tap([(100, 240)])
    sleep(1)
    driver.find_element(By.XPATH, '//android.widget.ImageButton[@content-desc="确定"]').click()
    sleep(1)
    driver.find_element(By.XPATH, '//android.widget.TextView[@text="同时设置"]').click()
    sleep(1)
    os.system('adb shell input keyevent 3')


def debug():
    while True:
        print('进入显示设置界面')
        driver.start_activity('com.android.settings', '.Settings$DisplaySettingsActivity')
        sleep(5)
        print('进入无线设置界面')
        driver.start_activity('com.android.settings', '.Settings$WirelessSettingsActivity')
        sleep(5)
        # print('进入系统设置界面')
        # driver.start_activity('com.android.settings', '.Settings$HwSystemDashboardActivity')
        # time.sleep(5)


if __name__ == '__main__':
    download_ggr()
    # adb_setting()
    # set_sleep()
    # set_wallpaper()
