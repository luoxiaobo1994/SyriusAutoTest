# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/9 22:34
# Desc: 测试前，检查机器人环境是否正常。

import re

from utils.connect_linux import *

robot = {
    '雷龙-齐达内': '10.2.8.65',
    '雷龙-内马尔': '10.2.8.57',
    '雷龙-苏亚雷斯': '10.2.9.181',
    '梁龙-佐助': '10.2.8.103'
}


def check_info(name):
    print(Linux_command(name, 'cat /etc/syrius/ota/version', index=1, name=f'机器人[{name}]的MoveBase-Version:'))
    print(Linux_command(name, 'cat /opt/syrius/ota/checker/application.yml', index=1, need='env: test'))
    print(Linux_command(name, 'cat /sys/robotInfo/RobotSN', index=1, name=f'机器人[{name}]SN:'))
    if Linux_command(name, 'ls -lh /etc/syrius/calibration_result/robot_sensors.yaml', index=1, name='标定文件检查：'):
        print(f"机器人[{name}]的标定文件检查：正常。")
    else:
        print(f"机器人[{name}]的标定文件已丢失，请检查！！！！")


def check_disk(name):
    res = Linux_command(name, 'df | head -2 | grep /')
    percent = re.findall('\d+%', res)[0]
    print(f"机器人[{name}]的磁盘当前使用：{percent}")


def check_battery(name):
    cmd = 'dbus-send --system --print-reply=literal --type=method_call --dest=com.syriusrobotics.holter /buzzard/holter com.syriusrobotics.holter.IHolter.getBattery'
    res = Linux_command(name, cmd)
    data = res.split()[-1]
    print(f"机器人[{name}]的当前电量：{data}%")


def main(bot):
    check_info(bot)
    check_disk(bot)
    check_battery(bot)


if __name__ == '__main__':
    # check('雷龙-齐达内')
    # check_battery('雷龙-齐达内')
    # main('雷龙-齐达内')
    # check('雷龙-内马尔')
    # check('雷龙-苏亚雷斯')
    main('10.2.8.103')
