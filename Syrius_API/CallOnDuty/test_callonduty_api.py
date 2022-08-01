# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/29 17:00
# Desc: CallOnDuty的接口自动化测试


import pytest
from base.Requests_API import RequestUtil
from base.common import read_yaml


class Test_CallOnDuty:

    @pytest.mark.parametrize("caseinfo", read_yaml('test_case.yaml'))
    def test_get_site(self, caseinfo):
        print(caseinfo)
        # RequestUtil().all_request(caseinfo)
        # assert 1


if __name__ == '__main__':
    pass
