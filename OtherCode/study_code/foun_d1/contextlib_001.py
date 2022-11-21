# -*- coding:utf-8 -*-
# Author: LuoXiaoBo
# Time: 2022-11-21 23:14
# Desc: context来管理上下文

import contextlib


# 还不完善，等熟悉了功能，这部分需要补全一下。
@contextlib.contextmanager
def file_open(filename):
    print("file open")
    yield {}  # 这里执行实际逻辑
    print("file close")


with file_open("file1") as f_opened:
    print("file processing")
