# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/8/16 14:13
# Desc: allure测试报告样例

import os

import allure
import pytest


@allure.epic("测试allure使用")
@allure.feature("通用基础业务支持")
@allure.story("测试用例_001")
@allure.title("用例标题：我是test_sucess")
@allure.description("这是一个描述装饰器：我是成功用例")
def test_success():
    """ desc: This test success"""
    assert True


@allure.epic("测试allure使用")
@allure.feature("通用基础业务支持")
@allure.story("测试用例_001")
@allure.title("用例标题：我是test_failure")
# @allure.description("这是一个描述装饰器：我是失败用例")  # 和方法里的注释长文本冲突，这个优先级高些--也许是因为在前。
def test_failure():
    """ desc: This test fails"""
    assert False


@pytest.mark.parametrize('param,fname,story', [('参数1-路人甲', '通用业务支持', '用例_001'), ('参数2-9527', '通用业务支持', '用例_002')])
def test_dynamic(param, fname, story):
    allure.dynamic.feature(f"{fname}")
    allure.dynamic.story(f"{story}")
    assert True


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    pytest.main(['allure_demo.py'])
    os.system('allure serve D:\\tmp')
