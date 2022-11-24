# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/9/9 22:34
# Desc: 测试前，检查机器人环境是否正常。

import re

from base.common import *
from utils.connect_linux import *
from utils.log2 import Logger2

log = Logger2(file='check_robot_log.txt').get_logger()

model = ''

robot = {
    '雷龙-齐达内': '10.2.8.65',
    '雷龙-内马尔': '10.2.8.57',
    '雷龙-苏亚雷斯': '10.2.9.181',
    '梁龙-鸣人': '10.2.8.103'
}


def check_info(robot):
    # log.debug(Linux_command(robot, 'cat /etc/syrius/ota/version', index=1, name=f'机器人[{robot}]的MoveBase-Version:'))
    log.debug(
        Linux_command(robot, 'cat /opt/cosmos/bin/etc/ota/version', index=1, name=f'机器人[{robot}]的MoveBase-Version:'))
    log.debug(
        Linux_command(robot, "grep -E 'build date:(.*?)$' /etc/version.yaml", name=f'机器人[{robot}]的L4T-vendor构建日期:'))
    log.debug(Linux_command(robot, 'cat /sys/robotInfo/RobotSN', index=1, name=f'机器人[{robot}]SN:'))
    if Linux_command(robot, "grep -E 'Sensors:' /opt/cosmos/etc/calib/calibration_result/robot_sensors.yaml", index=1,
                     name='标定文件检查：'):
        log.debug(f"机器人[{robot}]的标定文件检查-新路径：正常。")
        return
    elif Linux_command(robot, "grep -E 'Sensors:' /etc/syrius/calibration_result/robot_sensors.yaml", index=1,
                       name='标定文件检查：'):
        log.debug(f"机器人[{robot}]的标定文件检查-旧路径：正常。")
    else:
        log.debug(f"机器人[{robot}]的标定文件已丢失，请检查！！！！")


def check_time(robot, repair=True, count=5):
    while count > 0:
        res = Linux_command(robot, "date +'%Y-%m-%d %H:%M:%S'", just_result=True)
        log.debug(f"机器人[{robot}]当前时间:{res}")
        now = str(datetime.now())
        if res[:10] != now[:10]:
            log.warning(f"机器人[{robot}]当前时间与实际UTC时间差距较大，请检查！！！")
            now1 = list(time.localtime())
            date = ''.join([str(i) for i in now1[:3]])
            h = now1[3] - 8
            m = now1[4]
            s = now1[5]
            writetime = date + ' ' + ':'.join([str(h), str(m), str(s)])
            # print(writetime)
            if repair:
                log.debug(f"脚本即将设置时间到当前时间:{writetime}，时间时区为UTC0。")
                Linux_command(robot, f'sudo date -s "{writetime}"')
            count -= 1
        else:
            return 1


def check_disk(robot):
    res = Linux_command(robot, 'df | head -2 | grep /')
    percent = re.findall('\d+%', res)[0]
    log.debug(f"机器人[{robot}]的磁盘当前使用:{percent}")
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
    res1 = Linux_command(robot, 'cat /opt/cosmos/bin/ota/checker/application.yml', index=1, need='env: test')
    res2 = Linux_command(robot, 'cat /opt/cosmos/bin/iot-gateway/application.yml', index=1, need='env: test')
    res3 = Linux_command(robot, 'cat /opt/cosmos/bin/secbot/secbot/application.yml', index=1, need='env: test')
    if all([res1, res2, res3]) and 'test' in res1:
        log.debug(f"机器人[{robot}]的环境为：{res1}")
    else:
        log.debug(f"机器人[{robot}]的环境文件缺失，手动添加配置文件。")
        cmd = "sudo echo 'env: test' > /opt/cosmos/bin/ota/checker/application.yml"
        Linux_command(robot, cmd)
        cmd2 = "sudo echo 'env: test' > /opt/cosmos/bin/iot-gateway/application.yml"
        Linux_command(robot, cmd2)
        cmd3 = "sudo echo 'env: test' > /opt/cosmos/bin/secbot/secbot/application.yml"
        Linux_command(robot, cmd3)


def check_server(robot):
    cmd = 'ps -ef | grep navigation'
    res = Linux_command(robot, cmd, just_result=True)
    log.debug(res)


def make_file(robot):
    log.debug(Linux_command(robot, 'touch SQA测试机器人请勿乱改动.txt', isreturn=True))
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
        log.debug(f"机器人[{robot}]Model是：{res}，对应机型：{model[res] if model.get(res) else '没有对应机型，请检查。'}")
    except TypeError:
        log.warning(f"机器人[{robot}]Model查询结果返回异常，请检查。")


def check_skill(robot):
    res = get_resset(robot, 'ls /opt/cosmos/bin')
    # 把需要检查的文件丢在下面这个集合里，后面的逻辑会处理校验。
    necessary_file = {'calibration_skill', 'inuitive_xusb_detector', 'pulseaudioman ', 'health_skill',
                      'mapping_skill ', 'gadgetman', 'jinglebell', 'navigation_skill', 'psyche'}
    # print(res)  # 得到的结果，包含制表符和换行符。['bootstrapper\t  mapping_skill   secbot\r\n',  iot-gateway\t\t...]
    if len(necessary_file & res) == len(necessary_file):
        log.debug(f"机器人[{robot}] /opt/cosmos/bin目录下的文件与预设的检查项一致。")
    else:
        log.warning(f"机器人[{robot}] /opt/cosmos/bin目录下的文件与预设的检查项不一致，缺少以下文件:"
                    f"\n{necessary_file.difference(res)}")


def check_java(robot):
    res = get_resset(robot, 'ls /opt/cosmos/bin/keyring/keyring')
    necessary_file = {'stop.sh', 'run.sh'}
    if 'keyring' in ''.join(res) and necessary_file & res == necessary_file:
        log.debug(f"机器人[{robot}]下位机Java关键进程文件和jar包检查通过。")
        for i in res:
            if 'keyring' in i:
                log.debug(f"机器人[{robot}]的keyring版本是：{i}")

    else:
        log.debug(f"机器人[{robot}]下位机Java关键进程文件和jar包检查异常。查询到的文件如下：{res}")


def check_iot(robot):
    res = get_resset(robot, 'ls /opt/cosmos/bin/iot-gateway')
    necessary_file = {'stop.sh', 'run.sh'}
    if 'iot-gateway' in ''.join(res) and necessary_file & res == necessary_file:
        log.debug(f"机器人[{robot}]下位机iot-getway关键进程文件和jar包检查通过。")
        for i in res:
            if 'iot-gateway' in i:
                log.debug(f"机器人[{robot}]的iot-gateway版本是：{i}")

    else:
        log.debug(f"机器人[{robot}]下位机iot-gateway关键进程文件和jar包检查异常。查询到的文件如下：{res}")


def check_kuafu(robot):
    res = get_resset(robot, 'ls /opt/cosmos/bin/kuafu')
    necessary_file = {'run.sh'}
    if 'kuafu_gateway_classic' in ''.join(res) and necessary_file & res == necessary_file:
        log.debug(f"机器人[{robot}]下位机kuafu_gateway_classic关键进程文件和jar包检查通过。")
        for i in res:
            if 'iot-gateway' in i:
                log.debug(f"机器人[{robot}]的kuafu_gateway_classic版本是：{i}")

    else:
        log.debug(f"机器人[{robot}]下位机kuafu_gateway_classic关键进程文件和jar包检查异常。查询到的文件如下：{res}")


def check_ota(robot):
    res = get_resset(robot, 'ls /opt/cosmos/bin/kuafu')
    necessary_file = {'run.sh'}
    if 'kuafu_gateway_classic' in ''.join(res) and necessary_file & res == necessary_file:
        log.debug(f"机器人[{robot}]下位机kuafu_gateway_classic关键进程文件和jar包检查通过。")
        for i in res:
            if 'iot-gateway' in i:
                log.debug(f"机器人[{robot}]的kuafu_gateway_classic版本是：{i}")

    else:
        log.debug(f"机器人[{robot}]下位机kuafu_gateway_classic关键进程文件和jar包检查异常。查询到的文件如下：{res}")


def get_resset(robot, commond):
    res = Linux_command(robot, commond, more_res=True)
    tmp_res = ''.join(res).replace('\t', '').replace('\n', '').replace('\r', '')  # 替换，分割，转集合。
    new_res = set(tmp_res.split())
    return new_res


def main(bot):
    check_info(bot)
    check_time(bot)
    check_disk(bot)
    # check_battery(bot)  # 电量命令变更
    clear_OTA(bot)
    check_id(bot)
    write_env(bot)
    check_model(bot)
    check_skill(bot)
    check_java(bot)
    check_iot(bot)
    check_kuafu(bot)
    # check_ota(bot)  # 和文档给的有点不一样。
    log.debug('-' * 80 + '\n')


if __name__ == '__main__':
    # main(robot['雷龙-齐达内'])
    # check_java(robot['雷龙-内马尔'])
    main(robot['雷龙-内马尔'])
    # main('10.2.8.118')
    # main('10.2.9.106')
    # main('10.2.9.39')
    # main(robot['雷龙-苏亚雷斯'])
    # main(robot['梁龙-鸣人'])
    # main('10.2.8.77')
    # main('10.2.8.90')
