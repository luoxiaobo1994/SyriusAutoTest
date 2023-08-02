# -*- coding: utf-8 -*-
# Author: LuoXiaoBo
# 2023/4/24 19:39
# Describe: 本地调试脚本

from base.common import *
from collections.abc import Iterable

class Student:

    def __iter__(self):
        pass

dp(isinstance(Student(),Iterable))
dp(hasattr(Student(),'__getitem__'))