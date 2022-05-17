# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/24 14:00

from selenium.webdriver.common.by import By

apppackages = 'com.syriusrobotics.platform.launcher/com.syriusrobotics.platform.jarvis.MainFlutterActivity'


emergency_stop = (By.XPATH,'//android.widget.ImageView[@content-desc="无法连接？"]')