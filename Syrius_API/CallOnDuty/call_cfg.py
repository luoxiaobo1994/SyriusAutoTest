# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/28 20:51
# Desc:  专门读取配置文件的

from base.common import read_yaml


def cfg():
    return read_yaml(file='callonduty_config')
