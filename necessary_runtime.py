# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/6/22 23:21
# Desc: 必要的运行库安装

import os

# 先设置下载源是清华源。
os.system("pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple")

runtime_list = [
    'selenium',
    'requests',
    'matplotlib',
    'pytest',
    'allure-pytest',
    'pytest-rerun',
    'Appium-Python-Client',
    'pytest-rerunfailures',
    'wcwidth',
    'paramiko',
    'pyaml'
]

# 安装必要的库，省得每次都手写。麻烦
for item in runtime_list:
    os.system(f"pip install {item}")
