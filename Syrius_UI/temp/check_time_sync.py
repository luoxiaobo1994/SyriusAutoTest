# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/2/28 10:14
# Desc: 检查机器人时钟同步进程，是否启动。

import time, datetime, pytz, re
from utils.mylog import Logger
from base.common import time_difference

from utils.ssh_linux import MySSH

log = Logger(name='Syrius', file='./checktime.txt')
with open('./checktime.txt', 'r', encoding='utf-8') as f:
    text = f.readlines()  # 多要些数据，不然可能会有：关闭ssh这种杂日志影响。
count = int(re.findall('第(\d+)次检查', ''.join(text))[-1]) + 1  # 计数器自动获取上次记录的最后次数，并加1


def main(robot):
    global count
    log.debug(f"第{count}次检查。")
    ssh = MySSH(ip=robot, logfile='./checktime.txt', timeout=60)
    # 检查MoveBase版本
    MoveBase = ssh.exe_cmd('cat /opt/cosmos/etc/ota/version')
    log.debug(f'MoveBase版本：{MoveBase}')
    # 检查L4T信息
    L4T_date = ssh.exe_cmd("grep -E 'build date:(.*?)$' /etc/version.yaml")
    L4t_version = ssh.exe_cmd('cat /etc/jurassic_release')
    if L4t_version:
        log.debug(f"L4T构建日期：{L4T_date}，版本：{L4t_version}")
    else:
        log.debug(f"L4T构建日期：{L4T_date}。")
    # 检查SN
    SN = ssh.exe_cmd('cat /sys/robotInfo/RobotSN')
    SN = SN.split()[0].split()[0]  # 直接替换换行符有点问题。去两次，才能去掉所有空格。
    log.debug(f"机器人的SN：{SN}")
    # 检查ID
    ID_res = ssh.exe_cmd('dbus-send --system --print-reply=literal --type=method_call --dest=com.'
                         'syriusrobotics.secbot /buzzard/secbot com.syriusrobotics.secbot.ISecBot.getDroidId')
    ID = ID_res.split()[0]
    if ID == 'Error' or len(ID) <= 30:  # 长度是32的数字字母组合，如：747cd6f5d33e4c1cac045de78852c79d
        log.warning(f"机器人的ID异常，请检查一下，拿到的值：{ID}")  # 去掉  int32 0
    else:
        log.debug(f"机器人的ID：{ID}")
    # 检查Java进程数量
    java_process = ssh.exe_cmd('ps -aux | grep java | wc -l')
    if java_process >= '10':
        log.debug(f"Java进程数量：{java_process}，{'正常。'}")
    else:
        log.warning(f"Java进程数量：{java_process}，{'正常。'}")
    is_time_sync = ssh.exe_cmd("sudo systemctl is-active systemd-timesyncd").split('\r\n')
    if 'inactive' in is_time_sync:
        log.warning(f"当前机器人:[{robot}]时钟同步进程未开启：{is_time_sync[-1]}，有严重运行风险，请检查！！！", )
    else:
        log.debug(f"当前机器人:[{robot}]时钟同步进程为激活状态：{is_time_sync[-1]}，检查通过，进入重启流程。")

        # 检查机器人时间
        robot_time = ssh.exe_cmd("date +'%Y-%m-%d %H:%M:%S'")
        utc_time = datetime.datetime.now(pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S')  # '2023-02-06 03:10:39'
        log.debug(f"机器人时间：{robot_time}，UTC—0时间：{utc_time}")  # 拿到的时间：2023-02-06 03:05:10
        time_gap = time_difference(robot_time, utc_time)  # 机器人时间与当前UTC0时间差距。
        if time_gap[-1] > 10:
            log.warning(f"机器人当前时间：{robot_time}，与本机的时间差(UTC+0)是：{time_gap[0]}天{time_gap[-1]}秒。")
            log.warning(f"机器人当前时间与实际UTC时间差距较大，请检查！")
        else:
            log.debug(f"机器人当前时间：{robot_time}，与本机的时间差(UTC+0)是：{time_gap[-1]}秒。")
        pad_robot_timestamp = ''
        date_command = "adb shell date +%s%3N && date +%s%3N"
        try:
            pad_robot_timestamp = ssh.exe_cmd(date_command).split()[-2:]  # 取最后俩，因为首次启动adb 会有杂七杂八的数据影响。
            if pad_robot_timestamp[0][-2:] == '3N':  # 安卓版本的时间戳获取会异常，3N不能正常转化。
                pad_timestamp = pad_robot_timestamp[0].replace('3N', '')  #
                robot_timestamp = pad_robot_timestamp[1][:len(pad_timestamp)]
                time_diff = abs(int(pad_timestamp) - int(robot_timestamp))  # 这种情况下，拿到的时间差是秒。
                if time_diff >= 2:
                    log.warning(f"上下位机的时间戳相差超过2s，请检查一下。")
                else:
                    log.debug(f"上下位机的时间戳相差为：{time_diff}秒。")
            else:
                time_diff = abs(int(pad_robot_timestamp[0]) - int(pad_robot_timestamp[1]))  # 这种情况下，拿到的时间差是毫秒。
                if time_diff > 2000:
                    log.warning(f"上下位机的时间戳相差超过2s，请检查一下。")
                else:
                    log.debug(f"上下位机的时间戳相差为：{time_diff}毫秒。")
        except Exception as e:
            log.warning(f"获取时间命令：{date_command}返回结果异常，请检查：{pad_robot_timestamp}。异常类型：{e}。")
    log.debug(f"检查完成，执行重启操作。")
    ssh.exe_cmd("sudo reboot")
    time.sleep(30)
    log.debug(f"当前机器人:[{robot}]重启完成，执行下一次循环。\n")
    count += 1
    del ssh  # 有必要手动销毁对象，不然循环里的对象，一直用一个，会导致脚本使用的内存，对象出问题。 产生连接异常。



if __name__ == '__main__':
    robot = {
        '雷龙·内马尔': '10.2.8.255',
        '雷龙·布里茨': '10.2.9.125',
        '梁龙1-鸣人': '10.2.8.103',
    }
    while True:
        try:
            # main(robot['雷龙·内马尔'])
            main(robot['雷龙·布里茨'])
            # main(robot['梁龙1-鸣人'])
            # break
        except Exception as e:
            log.error(f"检查流程，发生异常：{e}，跳过本次循环。")
            time.sleep(30)
        except KeyboardInterrupt:
            log.debug(f"手动停止脚本，停止检查。")
