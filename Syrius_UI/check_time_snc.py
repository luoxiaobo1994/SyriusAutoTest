# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/2/22 14:20
# Desc:

from utils.ssh_linux import *

def main(robot_ip):
    sshLogin(robot_ip)
    while True:
        is_time_sync = exe_cmd("systemctl is-active systemd-timesyncd").split('\r\n')
        if 'inactive' in is_time_sync:
            pp(f"当前机器人时钟同步进程未开启：{is_time_sync[-1]}，有严重运行风险，请检查！！！", 'WARNING', 'r')
        else:
            pp(f"当前机器人时钟同步进程为激活状态：{is_time_sync[-1]}，注意检查时钟同步情况。")
        time.sleep(10)
    sshClose()

if __name__ == '__main__':
    main('10.2.9.82')