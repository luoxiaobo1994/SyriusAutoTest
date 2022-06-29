# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/13 15:57
# Desc:  平板出厂设置

from app import APP
from base.common import *
from pages.pad_setings_page import *
from utils.log import logger


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
                                activity='com.android.settings startActivity')  # 自己获取安卓版本
        logger.info(f"脚本当前连接的平板:{device},安卓版本：{get_android_version(device)},Appium端口:{appium_port}")
        return browser

    def device_num(self):
        num = 0  # 序号从0开始
        devices_ls = get_devices()
        try:
            return devices_ls[num], 4725 + num * 5  # 每个设备之间，间隔5个以上
        except:
            logger.warning("获取设备UDID失败了,检查一下.")

    def set_sleep(self):
        # 设置屏幕休眠时间的
        # self.driver.start_activity('com.android.settings', '.Settings$DisplaySettingsActivity')  # 跳转到显示设置界面
        self.driver.click_element(*display_setting, i=True)
        self.driver.click_element(*sleep_time, i=True)
        print(111)

    def set_time(self):
        # 设置平板时区
        pass

    def adb_settings(self):
        # 能用adb设置的部分
        # 关闭自动旋转.
        cmd = 'adb shell content insert --uri content://settings/system --bind name:s:accelerometer_rotation --bind value:i:0'
        os.system(cmd)
        # 卸载智慧语音
        os.system('adb shell pm uninstall --user 0 com.huawei.vassistant')

    def setting_wallpaper(self):
        png = 'SyriusLogo.jpeg'
        os.system(f'adb push {png} /sdcard/Pictures')
        self.driver.find_element()

    def install_ggr(self):
        # 先拿到最新版的生产软件
        pass
        # 通过adb直接安装到平板内.

    def main(self):
        # 运行主函数
        self.adb_settings()
        self.set_sleep()


if __name__ == '__main__':
    pad = PadSettings()
    pad.main()
