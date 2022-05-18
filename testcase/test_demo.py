# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/18 22:27
# Desc: pytestdemo

import pytest


class TestDemo():

    @pytest.mark.parametrize('param',['aaa','bbb'])
    def test_a(self,param):
        print(f"test_1:{param}")
        assert 1

    @pytest.mark.parametrize('user',['lxb','root'])
    @pytest.mark.parametrize('pwd',['123456','111333'])
    def test_2(self,user,pwd):
        print(f'user:{user}')
        print(f'pwd:{pwd}')
        assert 0