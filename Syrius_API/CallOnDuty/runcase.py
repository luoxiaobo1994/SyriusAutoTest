# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/8/3 18:57
# Desc:  运行pytest的用例

import os

import pytest

if __name__ == '__main__':
    pytest.main(['test_callonduty_api.py'])
    os.system(r'allure generate D:\tmp -o ./report --clean')
