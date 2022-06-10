# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/1/4 20:11
import os
from utils.connect_linux import ssh
from multiprocessing.dummy import Pool
from utils.log import Logger

logger = Logger().get_logger()

devices = {
    # 填写你的机器人IP和机器人对应平板的IP.可以通过脚本,快速连接机器人,打开平板远程连接功能.
    '10.2.8.65': '10.2.10.229',  # device_ip : pad_ip
    # '10.2.9.39': '10.2.10.35',  # 高版梁龙
    # '10.2.8.57': '10.2.11.51',  # MLDM2449011108
    # '10.2.9.181': '10.2.11.119',
    # '10.2.8.118': '10.2.16.137',
    # '10.2.8.242': '10.2.11.107'  # 梁龙
    # '10.2.8.103': '10.2.10.9'  # 梁龙
    # '10.2.9.18': '10.2.16.163'  # 雷龙1604

}


def all_connect(ip):
    cmds = ['adb devices', "adb tcpip 5555"]  # 连上机器人需要执行的命令。
    # for i in devices.keys():
    res = ssh(ip=ip, cmds=cmds)  # 正常返回成功与否..
    if res:
        # 这里面,命令执行会有长时间连接不上的情况.平板连接了其他WIFI,导致IP不对.
        info = os.popen(f"adb connect {devices[ip]}").readlines()  # 连接对应的平板.
        logger.debug(info[0])
    else:
        logger.warning(f"设备:{ip},连接失败!!!")

    # print(f"共连接成功:{len(get_devices())}个设备.")  # 多线程会重复打印.


def is_alive(ip):
    # 只是调试设备是否开启.并打开tcpip端口.
    num = 0
    # cmds = ["adb devices", "adb tcpip 5555"]  # 连上机器人需要执行的命令。
    # for i in devices.keys():
    x = ssh(ip=ip, cmds='')
    if x:
        num += 1
    # print(f"共{num}个机器人已经启动.")


def just_adb(i):
    # for i in devices.values():
    os.system(f"adb connect {i}")


if __name__ == '__main__':
    os.system("adb devices")  # 先保证adb在本机启动.
    pool = Pool(len(devices))  # 线程数量根据设备数量来定.
    pool.map(all_connect, devices.keys())  # 连接你的机器人,并打开它对应平板的TcpIP端口,再把平板连接到大当前电脑上.多试几次.
    # pool.map(is_alive, devices.keys())  # 只是查看有多少个设备上电了.
    # pool.map(just_adb, devices.values())  # 只是连接机器人平板.
    # print(len(get_devices()))  # 查看我的电脑连接了几个机器人平板.
