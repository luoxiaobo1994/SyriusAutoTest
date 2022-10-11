# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/9 22:34
# Desc: 测试前，检查机器人环境是否正常。

import re

from utils.connect_linux import *
from utils.log2 import Logger2

log = Logger2(file='check_robot_log.txt').get_logger()

robot = {
    '雷龙-齐达内': '10.2.8.65',
    '雷龙-内马尔': '10.2.8.57',
    '雷龙-苏亚雷斯': '10.2.9.181',
    '梁龙-佐助': '10.2.8.103'
}


def check_info(robot):
    log.debug(Linux_command(robot, 'cat /etc/syrius/ota/version', index=1, name=f'机器人[{robot}]的MoveBase-Version:'))

    log.debug(
        Linux_command(robot, "grep -E 'build date:(.*?)$' /etc/version.yaml", name=f'机器人[{robot}]的L4T-vendor构建日期:'))
    log.debug(Linux_command(robot, 'cat /sys/robotInfo/RobotSN', index=1, name=f'机器人[{robot}]SN:'))
    log.debug(Linux_command(robot, 'touch SQA测试机器人请勿乱改动.txt', isreturn=True))
    if Linux_command(robot, 'ls -lh /etc/syrius/calibration_result/robot_sensors.yaml', index=1, name='标定文件检查：'):
        log.debug(f"机器人[{robot}]的标定文件检查：正常。")
    else:
        log.debug(f"机器人[{robot}]的标定文件已丢失，请检查！！！！")


def check_disk(robot):
    res = Linux_command(robot, 'df | head -2 | grep /')
    percent = re.findall('\d+%', res)[0]
    log.debug(f"机器人[{robot}]的磁盘当前使用：{percent}")
    threshold = '85%'
    if percent > threshold:
        log.debug(f"机器人[{robot}]的磁盘占用大于{threshold}，执行:1.日志清除命令。2.删除home目录下的更新包")
        Linux_command(robot, 'sudo journalctl --vacuum-size=1K')
        Linux_command(robot, 'rm -rf ./update_*')


def check_id(robot):
    res = Linux_command(robot, 'dbus-send --system --print-reply=literal --type=method_call --dest=com.'
                               'syriusrobotics.secbot /buzzard/secbot com.syriusrobotics.secbot.ISecBot.getDroidId')
    id = res.split()[0]
    log.debug(f"机器人[{robot}]的ID：{id}")


def check_battery(robot):
    cmd = 'dbus-send --system --print-reply=literal --type=method_call --dest=com.syriusrobotics.holter /buzzard/holter com.syriusrobotics.holter.IHolter.getBattery'
    res = Linux_command(robot, cmd)
    data = res.split()[-1]
    # print(data)
    log.debug(f"机器人[{robot}]的当前电量：{data}%")


def clear_OTA(robot):
    cmd = ['rm -rf /opt/syrius/cache/ota_client/downloader/*',
           'rm -rf /opt/syrius/cache/ota_client/facade/*']
    log.debug(f"清除机器人[{robot}]的OTA缓存。")
    for i in cmd:
        Linux_command(robot, i)


def write_env(robot):
    res1 = Linux_command(robot, 'cat /opt/syrius/ota/checker/application.yml', index=1, need='env: test')
    res2 = Linux_command(robot, 'cat /opt/syrius/iot-gateway/application.yml', index=1, need='env: test')
    if all([res1, res2]):
        log.debug(f"机器人[{robot}]的环境为：{res1}")
    else:
        log.debug(f"机器人[{robot}]的环境文件缺失，手动添加配置文件。")
        cmd = "sudo echo 'env: test' > /opt/syrius/ota/checker/application.yml"
        Linux_command(robot, cmd)
        cmd2 = "sudo echo 'env: test' > /opt/syrius/iot-gateway/application.yml"
        Linux_command(robot, cmd2)


def check_server(robot):
    cmd = 'ps -aux | grep navigation_skill'
    res = Linux_command(robot, cmd)
    log.debug(res)


def main(bot):
    check_info(bot)
    check_disk(bot)
    check_battery(bot)
    clear_OTA(bot)
    check_id(bot)
    write_env(bot)
    log.debug('-' * 20)


if __name__ == '__main__':
    main(robot['雷龙-齐达内'])
    # check_server(robot['雷龙-齐达内'])
    # main(robot['雷龙-内马尔'])
    # main(robot['雷龙-苏亚雷斯'])
    # main(robot['梁龙-佐助'])
    # main('10.2.8.242')
    # main(robot['梁龙-佐助'])
