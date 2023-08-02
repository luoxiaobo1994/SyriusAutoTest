# -*- coding:utf-8 -*-
# Author: luoxiaobo
# 2023/4/20 21:21
# Describe: 模拟的数据

from faker import Faker

fk = Faker()
fk.email()

# 一个学生表，应该包含哪些数据？
# 学号，姓名，性别，出生年月，