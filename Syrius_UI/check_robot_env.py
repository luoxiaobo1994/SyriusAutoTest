# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/9 22:34
# Desc: 测试前，检查机器人环境是否正常。

from utils.connect_linux import *

robot = {
    '雷龙-齐达内': '10.2.8.65',
    '雷龙-内马尔': '10.2.8.57',
    '雷龙-苏亚雷斯': '10.2.9.181',
    '梁龙-佐助': '10.2.8.103'
}


def check(name):
    print(Linux_command(robot[name], 'cat /etc/syrius/ota/version', index=1, name='机器人MoveBase-Version:'))
    print(Linux_command(robot[name], 'cat /opt/syrius/ota/checker/application.yml', index=1, need='env: test'))
    print(Linux_command(robot[name], 'cat /sys/robotInfo/RobotSN', index=1, name='机器人SN:'))
    print(
        Linux_command(robot[name], 'ls -lh /etc/syrius/calibration_result/robot_sensors.yaml', index=1, name='标定文件检查：'))
    # print(Linux_command(robot[name], 'ls /abdd'))
    print(Linux_command(robot[name], 'df | head -2 | grep /', name='机器人内存占用情况：'))

    print('----检查完成---')


# check('雷龙-齐达内')
check('雷龙-内马尔')
# check('雷龙-苏亚雷斯')
# check('梁龙-佐助')
