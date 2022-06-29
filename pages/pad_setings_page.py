# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/6/14 16:40
# Desc:

import requests
from selenium.webdriver.common.by import By

# 最新版GGR下载地址
ggr_url = 'https://download.flexgalaxy.com/gogoready/latest/index.html'
download = 'https://download.flexgalaxy.com/launcher-latest-prod.apk'
requests.get(url=download)

# 设置休眠时间相关
display_setting = (By.XPATH, '//android.widget.TextView[@text="休眠"]')  # resource-id:android:id/title
#  '10 分钟','15 秒' .
sleep_time = (By.XPATH, '//android.widget.CheckedTextView[@text="永不"]')  # resource-id:com.android.settings:id/text1

# 设置壁纸相关
wallpaper_setting = (By.XPATH, '//android.widget.TextView[@text="壁纸"]')
select_wallpaper = (By.XPATH, '//android.widget.TextView[@text="设置壁纸"]')
photo_album = (By.XPATH, '//android.view.View[@content-desc="图库"]')  # 设置界面的图库
pictures = (By.XPATH, '//android.widget.TextView[@text="图片"]')
picture_cancel = (By.XPATH, '//android.widget.ImageButton[@content-desc="取消"]')  # 这个坐标下面一点,是首个图片
picture_confirm = (By.XPATH, '//android.widget.ImageButton[@content-desc="确定"]')
select_picture = (By.XPATH, '//android.view.View[@content-desc="选择图片"]')  # 图片展示页面的标题. 做校验使用.
first_picture = [100, 240]  # 首张照片的坐标.
all_set = (By.XPATH, '//android.widget.TextView[@text="同时设置"]')

# 界面activity
display_page = '.Settings$DisplaySettingsActivity'  # 设置休眠使用
wireless_page = '.Settings$WirelessSettingsActivity'
sys_page = '.Settings$HwSystemDashboardActivity'  # 设置时间使用

# 设置时区
time_zone = (By.XPATH, '//android.widget.TextView[@text="日期和时间"]')
switch_button = (By.XPATH, '//android.widget.Switch')  # 4个,顺序如下:自动确定日期和时间,自动确定时区,24小时制,双时钟
zone_select = (By.XPATH, '//android.widget.TextView[@text="时区"]')
zone_list = (By.XPATH, '//android.widget.TextView[@text="???"]')  # 填写你的目标时区.上下滑动去找.
search_btn = (By.XPATH, '//android.widget.EditText[@text="搜索" and @resource-id="android:id/search_src_text"]')

# 坐标点
location = {'system_setting': [200, 1650], 'display_setting': [200, 900]}
options = {'language_input': [500, 600], 'time_zone': [600, 600], 'sys_sleep': [600, 400], 'wallpaper': [570, 750]}
