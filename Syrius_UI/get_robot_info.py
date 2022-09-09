# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/8 13:31
# Desc: 获取机器人相关信息

import os

info = {}


def get_info():
    MoveBase_version = cat_file("/etc/syrius/ota/version")
    robot_env = cat_file("/opt/syrius/ota/checker/applicationq.yml")
    robot_sn = cat_file('/sys/robotInfo/RobotSN')
    robot_id = 1
    calibration = cat_file('/etc/syrius/calibration_result/robot_sensors.yaml')


def cat_file(file):
    try:
        return os.popen(f"cat {file}").readlines()[0].replace('\n', '')
    except:
        return 'No data!'


def dbus_cmd(cmd):
    try:
        return os.popen(f"{cmd}").readlines()[0].replace('\n', '')
    except:
        return 'No data!'


if __name__ == '__main__':
    get_info()
