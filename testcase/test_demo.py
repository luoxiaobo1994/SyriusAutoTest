# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/18 22:27
# Desc: pytestdemo
import os

import pytest
import allure


class TestDemo():

    @allure.title('单个参数的参数化测试,')
    @pytest.mark.parametrize('param', ['aaa', 'bbb'])
    def test_a(self, param):
        """ 测试单个参数的参数化测试 """
        print(f"test_1:{param}")
        assert 1

    @allure.title('多个参数的参数化测试')
    @pytest.mark.parametrize('user', ['lxb', 'root'])
    @pytest.mark.parametrize('pwd', ['123456', '111333'])
    def test_2(self, user, pwd):
        """ 测试多个参数的参数化 """
        print(f'user:{user}')
        print(f'pwd:{pwd}')
        assert user and pwd

    @allure.title("测试错误的账号密码登陆")
    @pytest.mark.parametrize('user,pwd', [('123', '456'), ('12363', '')])
    def test_login_failed(self, user, pwd):
        user_list = ['lxb', 'root']
        assert user not in user_list


if __name__ == '__main__':
    pytest.main()
    # os.system()
