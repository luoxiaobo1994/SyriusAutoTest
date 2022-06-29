# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/12/9 14:40


from selenium.webdriver.common.by import By

"""
文本全是android.view.View的有：[前往，货架点信息，暂停按钮，顶部的拣货中也是，商品图片，拣货数量，商品条形码，商品名称，推荐点位，异常上报按钮，异常类型也是]	
载物箱已满?，订单详情，输入按钮，请拣取正确货品并扫码]
条形码输入框，商品输入框，载物箱输入框都是这个：android.widget.EditText@text=[载物箱码，货品码]  # 可以不用text
图片：android.widget.Image   [货架方向箭头，载物箱图片]
二级通知的弹窗：
Jarvis图标,通知图标：android.widget.ImageView[@content-desc="机器人定位丢失"]
"""
"""
桌面图标：android.widget.ImageView，索引很多，电池图标，公司logo,小程序图标.


skillspace内信息：
每个小程序的词条：android.widget.RelativeLayout
小程序的名称，打开/下载/更新 文本：android.widget.TextView，
层级关系：
    - android.widget.RelativeLayout  # 词条
        - 小程序名称。  android.widget.TextView[@text="SpeedPicker"]
        - 小程序图标。  android.widget.ImageView  # 第一个就是界面上的x，可以点这个退出小程序。也可以直接点击返回。
        - 打开/下载/更新按钮。 android.widget.RelativeLayout
            -  打开下载更新文本  android.widget.TextView[@text="打开"]
        - 小程序介绍。  android.widget.TextView  为用户提供一个支持机器人执行在仓库场 景中，与拣货员协同配合，执行拣货业务 服务的小程序。
"""

"""
非SP页面的元素:
android.view.View[@content-desc]  : 日志上传完成(下位机),上传机器人日志,获取配置信息(完成),配置信息获取完成,
android.widget.Button[@content-desc="完成"]  : 同步配置完成界面的完成按钮.
android.widget.Button[@text=] : "CANCEL","CONFIRM",上传的确认询问框也是,
android.widget.CheckBox[@text=/sdcard/log/2022-01/2022-01-06],crash_jarvis_2021-12-20_15_15_11.trace,

"""

"""
其他一些重要数据:
1.如何从Jarvis Launcher界面启动SpeedPicker:
    难点:Speedpicker不能指向性定位.  找到解决办法---获取Jarvis主界面的content-desc文本.可以找到对应索引关系.
        找到是这样的:'11:09\n01月11日\n星期二\nSkillSpace\nMeadowMapper\nSpeedPicker'.可以解决启动SpeedPicker的问题.
2.如果退出其他界面,是否需要处理?
    首先,需要没有其他异常,有异常,我点了也起不来.所以,先检查有没有异常通知,起码保证,定位正常.能顺利启动.
    收日志界面,就需要收集完成,才能重启.
    最后,怎么返回主界面,保证界面有SpeedPicker,能点起来.
"""

view = (By.XPATH, "//android.view.View[@text='前往']")
