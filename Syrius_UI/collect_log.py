# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/10 10:19
# Desc: 收集上下位机日志脚本.

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


class CollectLog():

    def __init__(self):
        self.driver = self.init_driver()
        # sleep(10)  # 做一个长等待，没办法。加载慢。
        self.view = (By.XPATH, '//android.view.View')
        self.image = (By.XPATH, '//android.widget.ImageView')
        # self.config = self.get_cnfig()  # 流程开始之前读取一次配置就行了,不用每次都读取.

    def init_driver(self):
        device = self.device_num()[0]  # 10.111.150.202:5555 这种格式.
        appium_port = self.device_num()[1]
        # 在这里填入安卓版本,避免跑不起来.
        browser = GGR().browser(devices=device, platformversion=get_android_version(device),
                                port=appium_port)  # 自己获取安卓版本
        logger.info(f"脚本当前连接的平板:{device},安卓版本：{get_android_version(device)},Appium端口:{appium_port}")
        return browser

    def device_num(self):
        num = 0  # 序号从0开始
        devices_ls = get_devices()
        try:
            return devices_ls[num], 4725 + num * 5  # 每个设备之间，间隔5个以上
        except:
            logger.warning("获取设备UDID失败了,检查一下.")

    def get_text(self, wait=3, raise_except=False):  # 3s左右合理,有些流程跳转时,会转圈一会儿.
        count = 20  # 有个限制.
        while count > 0:
            count -= 1  # 避免死循环
            view_ls = self.driver.app_elements_text(self.view, wait)  # 拿到异常类型的文本。文本也是view.View类型的。
            try:
                view_ls = [i for i in view_ls if i != '']  # 去重。会抓到空文本。
                if view_ls:  # 抓到才出去.在sp里,必定是会有文本页面的.
                    return view_ls
                else:
                    if count % 10 == 0:  # 偶尔刷新一次.
                        # 判断是不是在Jarvis主界面.
                        try:
                            tmp_desc = self.driver.app_elements_content_desc()
                            if 'SkillSpace' in ''.join(tmp_desc):
                                logger.debug("当前在Jarvis主界面")
                        except:
                            pass  # The function needs to be improved
                        logger.info("当前页面没抓到文本,如果持续刷新这个日志,请前往检查一下.")
                        return  # 跳出去
            except TypeError:
                logger.debug("抓取文本发生类型错误异常,检查是否退出SP界面了.")
                if raise_except:
                    raise just_err
                sleep(5)
            except Exception as e:
                logger.info(f"抓取文本,出现了一些别的异常:{e}")
                return  # 跳出去
        if count == 0:
            logger.info(f"这个设备:{self.device_num()[0]}有一段时间没抓到文本了,去检查一下.")
            sleep(10)  # 这里也要睡眠一下，避免刷日志太快了。
            return  # 跳出去

    def get_content(self, wait=2):
        count = 20  # 有个限制.
        while count > 0:
            count -= 1  # 避免死循环
            view_ls = self.driver.app_elements_content_desc(self.view, wait)
            if view_ls:
                return [i for i in view_ls if i]
            else:
                count -= 1


