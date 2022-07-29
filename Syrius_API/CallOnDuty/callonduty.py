# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/10/27 16:02

import time

from appium import webdriver
from selenium.webdriver.common.by import By

from base.base_page import TestKey
from create_task import create_task
from utils.log import Logger

logger = Logger(file=f'log.txt').get_logger()

language = {"cn": "已完成，继续任务", "en": 'Completed, resuming the task'}
continue_btn = (By.XPATH, '//android.view.View[@text="%s"]' % language['cn'])
notask_btn = (By.XPATH, '//android.widget.Button[@text="退出"]')

app_data = {
    "platformName": "Android",
    "platformVersion": "10",  # 注意调试平板的安卓版本
    "udid": "10.2.10.9:5555",
    "deviceName": "k11",  # 注意调试平板的IP
    "apppackage": "com.syriusrobotics.platform.launcher",
    "appActivity": "com.syriusrobotics.platform.launcher/com.syriusrobotics.platform.jarvis.MainFlutterActivity",
    "noReset": True,
    "unicodeKeyboard": False,
    "resetKeyboard": False
}
browser = webdriver.Remote("http://localhost:4725/wd/hub", app_data)  # 注意修改这个端口号
# content = browser.contexts  # 定位H5元素,需要切换contexts
# browser.switch_to.context()  # 跳转目标
driver = TestKey(browser)
site = 'Def2ixiR'  # 旧的'PwQnQb69'
print('*' * 30 + "注意设置平板语言模式,选择正确的交互文本" + '*' * 30)
logger.debug(f"当前页面文本：{driver.app_elements_text((By.XPATH, '//android.view.View'))}")

count = 0
seq = 0
while True:
    speed = 5
    try:
        if driver.find_element(notask_btn, wait=1):  # 没有任务，就发一个任务做。
            wait_time = speed + 5  # 这里要单独多点时间
            create_task()
            logger.info(f"无任务，创建了场地{site}的99次循环任务。{wait_time}s后开始执行CallOnDuty.如果机器人不移动，注意检查场地信息。")
            time.sleep(wait_time)
    except:
        pass
    try:
        if driver.find_element(continue_btn, wait=speed + 0.5):
            time.sleep(speed)  # 给程序预留一个播报时间.
            logger.debug(f"当前页面文本：{driver.app_elements_text((By.XPATH, '//android.view.View'))}")
            driver.click_element(continue_btn, i=False)
            logger.debug(f"点击继续按钮，前往下一个任务点。")
            count += 1
            logger.info(f"当前循环，到达第{count}个目标点位")
        else:
            time.sleep(speed)  # 间隔检查元素.
    except:
        time.sleep(speed)  # 什么都抓不到，就过。
    if count == 5:
        seq += 1
        logger.debug(f"完成第{seq}次循环。")
        count = 0
