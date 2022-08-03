# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/29 17:00
# Desc: CallOnDuty的接口自动化测试


import pytest

from base.Requests_API import RequestUtil
from base.common import read_yaml


class Test_CallOnDuty:

    @pytest.mark.parametrize("param", read_yaml('test_case.yaml')['get_site'])
    def test_get_site(self, param):
        """ 获取场地信息 """
        # print(param)
        method = param['method']
        url = param['url']
        res = RequestUtil().all_request(url=url, method=method)
        assert res.status_code == 200

    @pytest.mark.parametrize("param", read_yaml('test_case.yaml')['get_site_err'])
    def test_get_site_err(self, param):
        """ 获取场地信息-反例 """
        # print(param)
        method = param['method']
        url = param['url']
        res = RequestUtil().all_request(url=url, method=method)
        print(param, f"res:{res}")
        assert str(res.status_code).startswith('4')

    @pytest.mark.parametrize("param", read_yaml('test_case.yaml')['get_task'])
    def test_get_task(self, param):
        """ 获取场地当前的任务信息 """
        method = param['method']
        url = param['url'].format(read_yaml('test_case.yaml')['site'])
        res = RequestUtil().all_request(url=url, method=method)
        assert res.status_code == 200

    @pytest.mark.parametrize("param", read_yaml('test_case.yaml')['get_task_err'])
    def test_get_task_err(self, param):
        """ 获取场地当前的任务信息-反例 """
        method = param['method']
        url = param['url'].format(read_yaml('test_case.yaml')['site'])
        res = RequestUtil().all_request(url=url, method=method)
        print(param, f"res:{res}")
        assert str(res.status_code).startswith('4')

    def test_get_taskdetail(self):
        """ 获取任务的详细信息 """
        print('')


if __name__ == '__main__':
    pass
