# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/12/19 10:28
# Desc: 监测GoGoReady CPU和内存占用情况。

import os, csv
import time
import numpy as np
from matplotlib import pyplot as plt

cpu_list = []
time_list = []
app_list = []
lines = []
package_name = []

def get_applist():
    global package_name
    with open('') as f:
        lines