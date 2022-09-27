# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/14 16:24
# Desc:

import os
from time import sleep
from appium import webdriver
from base.base_page import TestKey
from base.common import get_android_version
from pages.pad_setings_page import *

os.system(f'adb push {"SyriusLogo.jpeg"} /sdcard/Pictures')
sleep(5)

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

browser = TestKey(driver)


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
        browser.click_element(display_setting)
        browser.click_element(sleep_time)
    else:
        driver.find_element('//android.widget.TextView[@text="10 分钟"]')


def set_wallpaper():
    driver.start_activity('com.android.settings', '.Settings$DisplaySettingsActivity')
    browser.click_element(locator=wallpaper_setting, new_locator=select_wallpaper)  # 点击壁纸
    browser.click_element(locator=select_wallpaper, new_locator=photo_album)  # 点击设置壁纸
    browser.click_element(locator=photo_album, new_locator=pictures)  # 点击图片 --进入图片选择
    driver.tap([(100, 240)])  # 通过坐标选取首张
    browser.click_element(locator=picture_confirm, new_locator=all_set)  # 确定
    browser.click_element(locator=all_set)  # 设置完成
    os.system('adb shell input keyevent 3')  # 返回桌面


def set_time():
    os.system('adb shell am start com.android.settings startActivity')
    while True:
        driver.tap([(200, 1650)])
        if browser.element_display(time_zone):
            break
        else:
            sleep(0.5)


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
    # download_ggr()
    adb_setting()
    set_time()
    set_sleep()
    set_wallpaper()
