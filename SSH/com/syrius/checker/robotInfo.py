# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/9 22:34
# Desc: 测试前，检查机器人环境是否正常。

import re
from com.syrius.util.sshUtil import *
from loguru import logger

import sys
logger.remove()#删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
logger.add(sys.stderr, level="DEBUG")# level=TRACE,DEBUG,INFO,SUCCESS,WARNING,ERROR,CRITICAL





def dateToVersion(dateStr):
    """
    通过构建时间转化对应的版本信息
    :param dateStr:格式为：2022-11-27 09:39:45
    :return:版本信息
    """
    # 使用map存储对应版本号
    mapVersion = {
        "2022-11-27 09:39:45": "633"
    }
    versionStr = "0"
    for key in mapVersion:
        if dateStr in key:
            versionStr = mapVersion[key]
    return versionStr


def getL4TVendor(command=None):
    """
    获取V4TVendor的版本号
    :param command:获取版本号的指令
    :return:返回版本信息
    """
    if command is None:
        command = "cat /etc/version.yaml"
    robotSystemInfo = ssh_exe_cmd(command)
    # print(robotSystem)
    buildTime = re.findall('build date:\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', robotSystemInfo)
    versionStr = dateToVersion(buildTime[0][11:])
    resultStr = f"L4TVendor的版本号为：【{versionStr}】，构建时间：{buildTime[0]}"
    logger.info(resultStr)
    return resultStr


def getRobotSN(command=None):
    """
    获取robotSN的相关信息
    :return:
    """
    if command is None:
        command = "cat /sys/robotInfo/RobotSN"
    robotSystemInfo = ssh_exe_cmd(command)
    robotSystemInfo = re.findall('\w+', robotSystemInfo)
    resultStr = f"RobotSN为：【{robotSystemInfo[0]}】"
    logger.info(resultStr)
    return resultStr


def getRobotModeName(modeName):
    """
    通过mode获取机器的型号
    :param modeName:
    :return:
    """
    modeNameMap = {
        "LLLBR0200": "BRONTO",
        "OVAVE0100": "VEGA",
        "OVAVE0200": "VEGA",
        "OSERA0100": "Rachel",
        "LLLPO0100": "波塞冬",
        "LMLDI0100": "梁龙(矮版)",
        "LMLDI0101": "梁龙(高版)",
        "LMLDI0300": "梁龙1.1/梁龙1A(矮版)",
        "LMLDI0301": "梁龙1.1/梁龙1A(高版)",
        "LMLDI0400": "梁龙2(矮版)",
        "LMLDI0401": "梁龙2(高版)",
        "LMLDI0500": "梁龙2(矮版+认证)",
        "LMLDI0501": "梁龙2(高版+认证)",
        "LMLDI0200": "梁龙2A(矮版)",
        "LMLDI0201": "梁龙2A(高版)",
        "LMLDI0600": "梁龙2A(矮版+认证)",
        "LMLDI0601": "梁龙2A(高版+认证)",
        "OSCRI0100": "RIGEL",
        "LMLBA0100": "重龙(PA版)",
        "LMLBA0200": "重龙(工业版)"
    }
    result = "BRONTO"
    for key in modeNameMap:
        if modeName in key:
            result = modeNameMap[key]
    return result


def getModel(command=None):
    """
    获取Model的相关信息
    :return:
    """
    if command is None:
        command = "cat /sys/robotInfo/Model"
    robotSystemInfo = ssh_exe_cmd(command)
    robotSystemInfo = re.findall('\w+', robotSystemInfo)
    resultStr = f"Model为：【{robotSystemInfo[0]}】，该机器人的型号为：【{getRobotModeName(robotSystemInfo[0])}】"
    logger.info(resultStr)
    return resultStr

 
def getOTA(command=None):
    """
    获取OTA的版本信息
    :return:
    """
    if command is None:
        command = "cat /opt/cosmos/etc/ota/version"
    robotSystemInfo = ssh_exe_cmd(command)
    resultStr = f"OTA的版本为为：【{robotSystemInfo}】"
    logger.info(resultStr)
    return resultStr


def getENV(command=None):
    """
    获取下位机环境
    :return:
    """
    if command is None:
        command = "cat /opt/cosmos/bin/ota/checker/application.yml"
    robotSystemInfo = ssh_exe_cmd(command)
    resultStr = ""
    if "env: test" in robotSystemInfo:
        resultStr = "test"
    else:
        resultStr = "prod"

    resultStr = f"ENV为：【{resultStr}】"
    logger.info(resultStr)
    return resultStr


def main(addr):
    '''  登录信息拼接，开启链接 '''
    address = addr.split(":")
    ssh_login(address[0], address[1], "syrius", "syrius")

    ''' 获取对应的信息 '''
    getL4TVendor()
    getRobotSN()
    getModel()
    getOTA()
    getENV()

    ''' 关闭链接 '''
    closeSSH()


if __name__ == '__main__':
    robotMap = {
        '雷龙-齐达内': '10.2.8.65:22',
        '雷龙-内马尔': '10.2.8.57:22',
        '雷龙-苏亚雷斯': '10.2.9.181:22',
        '梁龙-佐助': '10.2.8.103:22',
        '电子平台1': '10.2.8.193:22'
    }

    # main(robot['雷龙-齐达内'])
    # check_server(robot['雷龙-苏亚雷斯'])
    # main(robot['雷龙-内马尔'])
    main(robotMap['电子平台1'])
    # main(robot['梁龙-佐助'])
    # main('10.2.8.77')
    # main('10.2.8.90')
    # main(robot['梁龙-佐助'])
