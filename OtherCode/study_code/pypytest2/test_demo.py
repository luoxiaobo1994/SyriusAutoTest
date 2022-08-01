# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/8/1 16:38
# Desc: pytest执行demo

import os, sys

# sys.path.append(r'\Users\luoxiaobo\PycharmProjects\SyriusAutoTest\base')
import pytest
from base.common import read_yaml

print(sys.path)


class Test_Demo():

    def setup_class(self):
        print("整个类执行之前的一次初始化，假定是启动了浏览器。\n")

    def teardown_class(self):
        print("\n整个类执行完之后，执行的一次扫尾操作，假定是关闭浏览器。")

    @pytest.mark.parametrize('params', read_yaml(file='./case_demo.yaml', key='login'))
    def test_login(self, params):
        print(f"测试登录功能:{params['name']}")
        print(f"登录信息：{params['data']}\n")

    @pytest.mark.parametrize('params', read_yaml(file='./case_demo.yaml', key='login_err'))
    def test_login_err(self, params):
        print(f"测试登录失败功能：{params['name']}")
        print(f"登录信息：{params['data']}\n")


if __name__ == '__main__':
    pytest.main(['test_demo.py'])
    os.system('allure generate ./temp -o ./report --clean')
    # print(read_yaml(file='./case_demo.yaml', key='login'))
