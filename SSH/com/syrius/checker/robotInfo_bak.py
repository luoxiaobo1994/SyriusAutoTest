# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/9 22:34
# Desc: 测试前，检查机器人环境是否正常。

import re
from com.syrius.util.sshUtil_bak import *
from loguru import logger

# from base.common import *
# from utils.connect_linux import *
# from utils.log2 import Logger2


# log = Logger2(file='check_robot_log.txt').get_logger()


robot = {
    '雷龙-齐达内': '10.2.8.65',
    '雷龙-内马尔': '10.2.8.57',
    '雷龙-苏亚雷斯': '10.2.9.181',
    '梁龙-佐助': '10.2.8.103'
}


def check_info(robot):
    # logger.debug(Linux_command(robot, 'cat /etc/syrius/ota/version', index=1, name=f'机器人[{robot}]的MoveBase-Version:'))
    logger.debug(
        Linux_command(robot, 'cat /opt/cosmos/bin/etc/ota/version', index=1, name=f'机器人[{robot}]的MoveBase-Version:'))
    logger.debug(
        Linux_command(robot, "grep -E 'build date:(.*?)$' /etc/version.yaml", name=f'机器人[{robot}]的L4T-vendor构建日期:'))
    logger.debug(Linux_command(robot, 'cat /sys/robotInfo/RobotSN', index=1, name=f'机器人[{robot}]SN:'))
    if Linux_command(robot, 'ls -lh /etc/syrius/calibration_result/robot_sensors.yaml', index=1, name='标定文件检查：'):
        logger.debug(f"机器人[{robot}]的标定文件检查：正常。")
    else:
        logger.debug(f"机器人[{robot}]的标定文件已丢失，请检查！！！！")


def check_time(robot, repair=True):
    res = Linux_command(robot, "date +'%Y-%m-%d %H:%M:%S'", justResult=True)
    logger.debug(f"机器人[{robot}]当前时间:{res}")
    now = str(datetime.now())
    if res[:10] != now[:10]:
        logger.warning(f"机器人[{robot}]当前时间与实际UTC时间差距较大，请检查！！！")
        now1 = list(time.localtime())
        date = ''.join([str(i) for i in now1[:3]])
        h = now1[3] - 8
        m = now1[4]
        s = now1[5]
        writetime = date + ' ' + ':'.join([str(h), str(m), str(s)])
        # print(writetime)
        if repair:
            logger.debug(f"脚本即将设置时间到当前时间:{writetime}，时间时区为UTC0。")
            Linux_command(robot, f'sudo date -s "{writetime}"')


def check_disk(robot):
    res = Linux_command(robot, 'df | head -2 | grep /')
    percent = re.findall('\d+%', res)[0]
    logger.debug(f"机器人[{robot}]的磁盘当前使用:{percent}")
    threshold = '85%'
    if percent > threshold:
        logger.debug(f"机器人[{robot}]的磁盘占用大于{threshold}，执行:1.日志清除命令。2.删除home目录下的更新包")
        Linux_command(robot, 'sudo journalctl --vacuum-size=1K')
        Linux_command(robot, 'rm -rf ./update_*')


def check_id(robot):
    res = Linux_command(robot, 'dbus-send --system --print-reply=literal --type=method_call --dest=com.'
                               'syriusrobotics.secbot /buzzard/secbot com.syriusrobotics.secbot.ISecBot.getDroidId')
    id = res.split()[0]
    logger.debug(f"机器人[{robot}]的ID：{id}")


def check_battery(robot):
    cmd = 'dbus-send --system --print-reply=literal --type=method_call --dest=com.syriusrobotics.holter /buzzard/holter com.syriusrobotics.holter.IHolter.getBattery'
    res = Linux_command(robot, cmd)
    data = res.split()[-1]
    # print(data)
    logger.debug(f"机器人[{robot}]的当前电量：{data}%")


def clear_OTA(robot):
    cmd = ['rm -rf /opt/syrius/cache/ota_client/downloader/*',
           'rm -rf /opt/syrius/cache/ota_client/facade/*']
    logger.debug(f"清除机器人[{robot}]的OTA缓存。")
    for i in cmd:
        Linux_command(robot, i)


def write_env(robot):
    res1 = Linux_command(robot, 'cat /opt/cosmos/bin/ota/checker/application.yml', index=1, need='env: test')
    res2 = Linux_command(robot, 'cat /opt/cosmos/bin/iot-gateway/application.yml', index=1, need='env: test')
    res3 = Linux_command(robot, 'cat /opt/cosmos/bin/secbot/secbot/application.yml', index=1, need='env: test')
    if all([res1, res2, res3]) and 'test' in res1:
        logger.debug(f"机器人[{robot}]的环境为：{res1}")
    else:
        logger.debug(f"机器人[{robot}]的环境文件缺失，手动添加配置文件。")
        cmd = "sudo echo 'env: test' > /opt/cosmos/bin/ota/checker/application.yml"
        Linux_command(robot, cmd)
        cmd2 = "sudo echo 'env: test' > /opt/cosmos/bin/iot-gateway/application.yml"
        Linux_command(robot, cmd2)
        cmd3 = "sudo echo 'env: test' > /opt/cosmos/bin/secbot/secbot/application.yml"
        Linux_command(robot, cmd3)


def check_server(robot):
    cmd = 'ps -ef | grep navigation'
    res = Linux_command(robot, cmd, justResult=True)
    logger.debug(res)


def make_file(robot):
    logger.debug(Linux_command(robot, 'touch SQA测试机器人请勿乱改动.txt', isReturn=True))
    Linux_command(robot, '')


def check_model(robot):
    model = {
        'LLLBR0200': '雷龙',  # 非正常添加，手动写的
        'LLLPO0100': '波塞冬',
        'LMLDI0100': '矮版梁龙-雅滕电机',
        'LMLDI0200': '矮版梁龙-自研电机',
        'LMLDI0101': '高版梁龙-雅滕电机',
        'LMLDI0201': '高版梁龙-雅滕电机',
        'LMLDI0400': '矮版梁龙2-雅滕电机-认证',
        'LMLDI0401': '高版梁龙2-雅滕电机-认证',
        'LMLDI0500': '高版梁龙2-雅滕电机-非认证',
        'LMLDI0501': '高版梁龙2-雅滕电机-非认证',
    }
    try:
        res = Linux_command(robot, 'cat /sys/robotInfo/Model')[:9]
        logger.debug(f"机器人[{robot}]Model是：{res}，对应机型：{model[res] if model.get(res) else '没有对应机型，请检查。'}")
    except TypeError:
        logger.warning(f"机器人[{robot}]Model查询结果返回异常，请检查。")


def main(bot):
    check_info(bot)
    check_time(bot)
    check_disk(bot)
    check_battery(bot)
    clear_OTA(bot)
    check_id(bot)
    write_env(bot)
    check_model(bot)
    logger.debug('-' * 50 + '\n')


if __name__ == '__main__':
    # main(robot['雷龙-齐达内'])
    # check_server(robot['雷龙-苏亚雷斯'])
    # main(robot['雷龙-内马尔'])
    main(robot['雷龙-苏亚雷斯'])
    # main(robot['梁龙-佐助'])
    # main('10.2.8.77')
    # main('10.2.8.90')
    # main(robot['梁龙-佐助'])