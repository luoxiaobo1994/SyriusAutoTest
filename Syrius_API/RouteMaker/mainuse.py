# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/1/19 14:39

import os

# 传入你地图文件的地址.地图ID/map_01/common 到这一级目录.
file = r'E:\工作\地图\有shel_location文件的地图\0ba791_cloud_03\map_01\common'
# 不要直接运行脚本,在pycharm里打开是看不到坐标的,只能看到图.使用命令行运行这个py文件
# ...\Syrius_API\RouteMaker>  python .\mainuse.py
os.system(f"Python route_ui.py {file}")


