# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/13 15:57
# Desc:  平板出厂设置

import os
import re
import traceback
from time import sleep
from selenium.webdriver.common.by import By
from GGR import GGR
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
        self.notify()  # 刷新一些提醒，避免遗漏配置。
        self.non_count = 0  # 界面抓到异常信息的计数器.
        # self.config = self.get_cnfig()  # 流程开始之前读取一次配置就行了,不用每次都读取.

    def init_driver(self):
        device = self.device_num()[0]  # 10.111.150.202:5555 这种格式.
        appium_port = self.device_num()[1]
        # 在这里填入安卓版本,避免跑不起来.
        browser = GGR().browser(devices=device, platformversion=get_android_version(device),
                                port=appium_port)  # 自己获取安卓版本
        logger.info(f"脚本当前连接的平板:{device},安卓版本：{get_android_version(device)},Appium端口:{appium_port}")
        return browser

    def notify(self):
        """ 脚本启动的一些注意事项提醒 """
        logger.debug("注意事项：1.SpeedPicker请开启快速拣货功能。\n2.注意平板连接到此电脑。\n3.注意先启动Appium服务。")

    def device_num(self):
        num = int(__file__.split('\\')[-1].split('.')[0].split('cn')[-1]) - 1  # 序号从0开始
        devices_ls = get_devices()
        try:
            return devices_ls[num], 4725 + num * 5  # 每个设备之间，间隔5个以上
        except:
            logger.warning("获取设备UDID失败了,检查一下.")
