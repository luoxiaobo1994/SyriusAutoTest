# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/13 15:57
# Desc:  平板出厂设置

import os
import re
import traceback
from time import sleep
from selenium.webdriver.common.by import By
from app import APP
from base.common import *
from utils.log import logger
from utils.file_reader import YamlReader
from Syrius_API.flagship.res_notify import send_order


class PadSettings():

    def __init__(self):
        self.driver = self.init_driver()
        # sleep(10)  # 做一个长等待，没办法。加载慢。
        self.view = (By.XPATH, '//android.view.View')
        self.image = (By.XPATH, '//android.widget.ImageView')
        self.non_count = 0  # 界面抓到异常信息的计数器.

    def init_driver(self):
        device = self.device_num()[0]  # 10.111.150.202:5555 这种格式.
        appium_port = self.device_num()[1]
        # 在这里填入安卓版本,避免跑不起来.
        browser = APP().browser(devices=device, platformversion=get_android_version(device),
                                port=appium_port, appname='com.android.settings',
                                activity='com.android.settings/.HWSettings')  # 自己获取安卓版本
        logger.info(f"脚本当前连接的平板:{device},安卓版本：{get_android_version(device)},Appium端口:{appium_port}")
        return browser

    def device_num(self):
        num = int(__file__.split('\\')[-1].split('.')[0].split('cn')[-1]) - 1  # 序号从0开始
        devices_ls = get_devices()
        try:
            return devices_ls[num], 4725 + num * 5  # 每个设备之间，间隔5个以上
        except:
            logger.warning("获取设备UDID失败了,检查一下.")

    def set_sleep(self):
        # 设置屏幕休眠时间的
        pass

    def set_time(self):
        # 设置平板时区
        pass

    def adb_settings(self):
        # 能用adb设置的部分
        # 卸载智慧语音
        os.system('adb uninstall ')
        # 锁定竖屏
        os.system('adb ')
        # 安装GGR

    def install_ggr(self):
        # 先拿到最新版的生产软件
        pass
        # 通过adb直接安装到平板内.


if __name__ == '__main__':
    pass
