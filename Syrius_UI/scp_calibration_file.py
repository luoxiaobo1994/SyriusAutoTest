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

file = 'E:\工作\数据保存\标定文件\\'
log = Logger(file='./temp/scp_calibration_file.txt')


def scp_file(robot, file):
    ssh = MySSH(robot, logfile='./temp/scp_calibration_file.txt')
    try:
        check_calibrationfile = ssh.exe_cmd(
            'sudo ls -lh /opt/cosmos/etc/calib/calibration_result/robot_sensors.yaml').split()
        if '/opt/cosmos/etc/calib/calibration_result/robot_sensors.yaml' in check_calibrationfile[-1]:
            ssh.log.debug(f"当前机器人：{robot}，标定文件已存在，退出流程。")
            ssh.log.debug(f"标定文件信息：{check_calibrationfile[-1]}")  # 要分行，只是美观罢了。
            return
    except:
        pass
    ssh.scp_file(file=file, path='./')
    ssh.exe_cmd('sudo cp robot_sensors.yaml /opt/cosmos/etc/calib/calibration_result/')
    ssh.exe_cmd('sudo chown factory:factory /opt/cosmos/etc/calib/calibration_result/robot_sensors.yaml')
    ssh.exe_cmd('sudo chmod 0600 /opt/cosmos/etc/calib/calibration_result/robot_sensors.yaml')
    ssh.exe_cmd('sudo setfacl -m u:pivot:rx -R /opt/cosmos/etc/calib/')
    ssh.exe_cmd('sync')
    res = ssh.exe_cmd('sudo ls -lh /opt/cosmos/etc/calib/calibration_result/robot_sensors.yaml').split()[-1]
    ssh.log.debug(f"执行后的标定文件情况：{res}")
    del ssh


# scp_file(robots['雷龙·内马尔'], file=file + r'\内马尔\robot_sensors.yaml')
# scp_file(robots['梁龙·鸣人'], file=file + r'\鸣人\robot_sensors.yaml')
# scp_file(robots['雷龙·苏亚雷斯'], file=file + r'\苏亚雷斯\robot_sensors.yaml')
# scp_file(robots['雷龙·布里茨'], file=file + r'\布里茨\robot_sensors.yaml')
scp_file(robots['网卡211'], file=file + r'\佐助\robot_sensors.yaml')
