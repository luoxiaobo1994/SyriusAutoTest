# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021-07-28 18:49
import os
import sys

path = os.path.abspath((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))
path2 = r'C:\Users\43811\PycharmProjects\SyriusAutoTest\OtherCode\study_code\pypytest2'
sys.path.append(path)
sys.path.append(path2)
import pytest


@pytest.fixture()
def setUp():
    print("这是前置函数")


@pytest.fixture()
def tearDown():
    print("这是后置函数")

# @pytest.fixture(scope='session', autouse=True)
# def driver():
#     global driver
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#
#     return driver
