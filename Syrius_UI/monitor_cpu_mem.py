# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/2/21 15:42
# Desc: 开启监控服务

import time
from utils.ssh_linux import MySSH
from utils.mylog import Logger

file = "E:\工作\测试资料\ServerAgent-2.2.3.zip"  # 工具在当前电脑的存放位置
log = Logger('scp_serverAgentLog.txt')


def startServerAgent(robot):
    ssh = MySSH(ip=robot, logfile='scp_serverAgentLog.txt')  # 日志文件，前后统一，就不会出事了。 
    have_file = ssh.exe_cmd('ls -l ServerAgent-2.2.3')
    # log.debug(f"have_file:{have_file}")
    if not have_file:
        log.debug(f"当前机器人：{robot}，还没有serverAgent工具。先传输文件到机器人。")
        ssh.scp_file(file=file, path='./')
        ssh.exe_cmd('unzip ServerAgent-2.2.3.zip')
    else:
        log.debug(f"当前机器人：{robot}，已经有serverAgent工具。直接开启测试。")
    ssh.exe_cmd('chmod +x ./ServerAgent-2.2.3/startAgent.sh')
    time.sleep(1)  # 等待一下。
    try:
        # res = ssh.exe_cmd('ServerAgent-2.2.3/startAgent.sh &', timeout=2)  #
        res = ssh.exe_cmd('python3 /home/developer/ServerAgent-2.2.3/startAgent.py', timeout=2)  #
        log.debug(f"执行开始脚本的结果：{res}")
    except TimeoutError:
        log.debug(f"startAgent.sh执行超时，请自行前往开启。")
    # check_is_alive = ssh.exe_cmd("ps -aux | grep '/bin/sh ./ServerAgent-2.2.3/startAgent.sh'")
    # log.debug(check_is_alive)


if __name__ == '__main__':
    robots = {
        # '雷龙·苏亚雷斯': '10.2.9.181',
        # '雷龙·内马尔': '10.2.8.255',
        '雷龙·布里茨': '10.2.9.125',
        # '雷龙·C罗': '10.2.8.118',
        '梁龙·鸣人': '10.2.8.103',
        # '网卡211': '10.2.8.211',
        # '梁龙·佐助': '10.2.8.77',
        '网卡82': '10.2.9.82',
        # '网卡242': '10.2.8.242',
    }
    for robot in robots:
        startServerAgent(robots[robot])
