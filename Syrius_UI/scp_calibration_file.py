# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/3/1 13:21
# Desc:

import os, time, re
from utils.ssh_linux import MySSH
from utils.mylog import Logger

robots = {
    '雷龙·苏亚雷斯': '10.2.9.181',
    '雷龙·内马尔': '10.2.8.255',
    '雷龙·布里茨': '10.2.9.125',
    '雷龙·C罗': '10.2.8.118',
    '梁龙·鸣人': '10.2.8.103',
    '网卡211': '10.2.8.211',
    '梁龙·佐助': '10.2.8.77',
    '网卡82': '10.2.9.82',
    '网卡242': '10.2.8.242',
}

log = Logger(file='./temp/scp_calibration_file.txt')


def scp_file(robot):
    ssh = MySSH(robot, logfile='./temp/scp_calibration_file.txt')
    ssh.scp_file(file='',path='/opt/cosmos/etc/calib/calibration_result/')
