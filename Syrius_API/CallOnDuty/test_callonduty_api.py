# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/29 17:00
# Desc: CallOnDuty的接口自动化测试

import allure
import pytest

from base.Requests_API import RequestUtil
from base.common import read_yaml


class Test_CallOnDuty:

    @allure.feature('获取环境下的场地信息')
    @allure.title("测试用例：获取场地")
    @pytest.mark.parametrize("param", read_yaml('test_case.yaml')['get_site'])
    def test_get_site(self, param):
        """ 获取场地信息 """
        # print(param)
        method = param['method']
        url = param['url']
        res = RequestUtil().all_request(url=url, method=method)
        # print(param, f"res--->{res},res.txt--->{res.text}")
        assert res.status_code == param['res_code']

    @allure.feature('获取环境下的场地信息')
    @allure.title("测试用例：获取场地异常流")
    @pytest.mark.parametrize("param", read_yaml('test_case.yaml')['get_site_err'])
    def test_get_site_err(self, param):
        """ 获取场地信息-反例 """
        # print(param)
        method = param['method']
        url = param['url']
        res = RequestUtil().all_request(url=url, method=method)
        # print(param, f"res--->{res},res.txt--->{res.text}")
        assert res.status_code == param['res_code']

    @allure.feature('获取环境下的场地任务列表')
    @allure.title("测试用例：获取场地任务列表")
    @pytest.mark.parametrize("param", read_yaml('test_case.yaml')['get_tasklist'])
    def test_get_task(self, param):
        """ 获取场地当前的任务信息 """
        method = param['method']
        url = param['url'].format(read_yaml('test_case.yaml')['site'])
        res = RequestUtil().all_request(url=url, method=method)
        # print(param, f"res--->{res},res.txt--->{res.text}")
        assert res.status_code == param['res_code']

    @allure.feature('获取环境下的场地任务列表')
    @allure.title("测试用例：获取场地任务列表异常流")
    @pytest.mark.parametrize("param", read_yaml('test_case.yaml')['get_tasklist_err'])
    def test_get_task_err(self, param):
        """ 获取场地当前的任务信息-反例 """
        method = param['method']
        url = param['url'].format(read_yaml('test_case.yaml')['site'])
        res = RequestUtil().all_request(url=url, method=method)
        # print(param, f"res--->{res},res.txt--->{res.text}")
        assert res.status_code == param['res_code']

    @allure.feature('获取环境下的场地任务详情')
    @allure.title("测试用例：获取场地任务详情")
    @pytest.mark.parametrize('param', read_yaml('test_case.yaml')['get_task'])
    def test_get_taskdetail(self, param):
        """ 获取任务的详细信息 """
        method = param['method']
        url = param['url'].format(read_yaml('test_case.yaml')['site'])
        data = param['data']
        res = RequestUtil().all_request(url=url, method=method, data=data)
        assert res.status_code == param['res_code']

    @allure.feature('获取环境下的场地任务详情')
    @allure.title("测试用例：获取场地任务详情异常流")
    @pytest.mark.parametrize('param', read_yaml('test_case.yaml')['get_task_err'])
    def test_get_taskdetail_err(self, param):
        """ 获取任务的详细信息 """
        method = param['method']
        url = param['url'].format(read_yaml('test_case.yaml')['site'])
        data = param['data']
        res = RequestUtil().all_request(url=url, method=method, data=data)
        assert res.status_code == param['res_code']


if __name__ == '__main__':
    pass
