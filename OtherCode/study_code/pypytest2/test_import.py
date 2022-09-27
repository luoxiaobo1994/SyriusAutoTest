# -*- coding:utf-8 -*-
# Author:LuoXiaoBo
# Time:2022-09-28 0:21
import pytest

from base.common import *

class TestImport():

    def test_get_time(self):
        print(get_time())
        assert 1==1

if __name__ == '__main__':
    pytest.main([__file__])
    # pytest.main(['-vs'])