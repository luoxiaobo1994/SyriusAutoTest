# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/3/3 17:14
# Desc: 练习画图


import pygal

view = pygal.Bar()
view.title = '柱状图'

view.add('数据',[1,8,4,2,9,4,7,3,1])
view.render_to_file('bar.svg')