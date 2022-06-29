# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/10/29 14:27
from selenium.webdriver.common.by import By

from GGR import GGR

driver = GGR().browser(devices='10.111.150.12:5555', port=4723)
image = driver.find_elements((By.XPATH, '//android.widget.ImageView'))
soft_index = driver.app_elements_content_desc((By.XPATH, '//android.view.View'))
sp_index = 0
for i in soft_index:
    print(f"i:{i}")
    if 'SpeedPicker' in i:
        x = i.split('\n')[::-1]
        print(f"x:{x}")
        sp_index = x.index('SpeedPicker') + 1  # 因为反过来了.从0开始.
        print(sp_index)

driver.click_one(image[-sp_index])  # 可以点击成功.
print("点了吗?")
