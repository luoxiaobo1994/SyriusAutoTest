# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/7 11:42
# Desc:

import pytest
import requests

base_url = 'http://127.0.0.1:8000/app01'


@pytest.mark.parametrize('nid', ['1', '2'])
def test_getuser(nid):
    res = requests.get(url=base_url + '/getuser' + f'?nid={nid}').json()
    print(res)
    assert 'code' in res
