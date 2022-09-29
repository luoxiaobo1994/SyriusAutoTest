# -*- coding:utf-8 -*-
# Author:LuoXiaoBo
# Time:2022-09-27 23:23

import pytest


class TestFirstDemo():

    def test_01_add(self):
        assert 1 + 1 == 2

    def test_01_sub(self):
        assert 2 - 1 == 1


if __name__ == '__main__':
    pytest.main([__file__])