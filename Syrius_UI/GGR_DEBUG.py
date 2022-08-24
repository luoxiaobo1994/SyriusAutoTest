# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/1/21 10:47

from time import sleep

from selenium.webdriver.common.by import By

from GGR import GGR
from base.common import *
from utils.log import Logger

logger = Logger(file=f'{get_devices()[0]}.txt').get_logger()


class Ggr_Debug():

    def __init__(self):
        self.driver = self.init_driver()
        # sleep(10)  # 做一个长等待，没办法。加载慢。
        self.view = (By.XPATH, '//android.view.View')
        self.image = (By.XPATH, '//android.widget.ImageView')
        self.TextView = (By.XPATH, '//*[@resource-id="com.syriusrobotics.platform.launcher:id/l_tv_title"]')

    def init_driver(self):
        device = self.device_num()[0]  # 10.111.150.202 这种格式.
        appium_port = self.device_num()[1]
        browser = GGR().browser(devices=device, platformversion='8', port=appium_port)
        print(f"Script connect Pad UDID:{device},Appium port:{appium_port}")
        return browser

    def device_num(self):
        num = 0  # 序号从0开始
        devices_ls = get_devices()
        try:
            return devices_ls[num], 4725 + num * 5  # 每个设备之间，间隔5个以上
        except:
            print("There is an error in getting the UDID of the device. Please check it.")

    def check_view_content(self):
        while True:
            try:
                print(f"view_content:{get_time()} {self.driver.app_elements_content_desc(self.view)}")
                sleep(3)
            except:
                pass

    def check_view_text(self):
        while True:
            try:
                print(f"view_text:{get_time()} {self.driver.app_elements_text(self.view)}")
                sleep(3)
            except:
                pass

    def check_image_text(self):
        while True:
            try:
                print(f"image_text:{get_time()} {self.driver.app_elements_text(self.image)}")
                sleep(3)
            except:
                pass

    def check_image_content(self):
        while True:
            try:
                print(f"image_content:{get_time()} {self.driver.app_elements_content_desc(self.image)}")
                sleep(3)
            except:
                pass

    def check_textView(self):
        while True:
            try:
                print(f"TextView:{get_time()} {self.driver.app_elements_text(self.TextView)}")
                sleep(3)
            except:
                pass


if __name__ == '__main__':
    gg = Ggr_Debug()
    t1 = threading.Thread(target=gg.check_image_text)
    t2 = threading.Thread(target=gg.check_image_content)
    t3 = threading.Thread(target=gg.check_view_text)
    t4 = threading.Thread(target=gg.check_view_content)
    t5 = threading.Thread(target=gg.check_textView)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
