# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/1/4 20:11
import os
import re
from multiprocessing.dummy import Pool

from utils.connect_linux import ssh
from utils.log import logger

devices = {
    # 填写你的机器人IP和机器人对应平板的IP.可以通过脚本,快速连接机器人,打开平板远程连接功能.
    # '10.2.8.65': '10.2.11.51',  # device_ip : pad_ip
    # '10.2.9.39': '10.2.10.35',  # 高版梁龙
    # '10.2.8.255': '10.2.11.51',  # MLDM2449011108
    '10.2.9.181': '10.2.11.119',  # 雷龙-苏亚雷斯
    # '10.2.8.118': '10.2.16.198',  # 雷龙-C罗
    # '10.2.8.77': '10.2.16.57',
    # '10.2.8.242': '10.2.11.107'  # 梁龙
    # '10.2.8.103': '10.2.10.9'  # 梁龙-鸣人
    # '10.2.9.18': '10.2.16.163'  # 雷龙1604

}


def all_connect(ip):
    # main(ip)
    cmds = ['adb devices', "adb shell ip addr show wlan0", "adb tcpip 5555"]  # 连上机器人需要执行的命令。
    res = ssh(ip=ip, cmds=cmds)  # 正常返回成功与否..
    # print(res)
    if res:
        if res[-1]:
            text = ''.join([str(i) for i in res])
            # 能抓到机器人平板IP的情况下。
            try:
                pad_ip = re.findall(r'inet (.*?)/', text)[0]  # 兜底抓到空的情况下
                logger.debug(f"当前机器人：{ip},实时连接的平板IP为：{pad_ip}.")
                info = os.popen(f"adb connect {pad_ip}").readlines()
                logger.debug(info[0])
            except:
                logger.warning(f"没有抓取到平板的实时IP。")
        else:
            # 抓不到实时的IP，就按默认的去连接。
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
    pool.map(all_connect, devices.keys())  # 连接你的机器人,并打开它对应平板的TcpIP端口,再把平板连接到当前电脑上.多试几次.
    # pool.map(is_alive, devices.keys())  # 只是查看有多少个设备上电了.
    # pool.map(just_adb, devices.values())  # 只是连接机器人平板.
    # print(len(get_devices()))  # 查看我的电脑连接了几个机器人平板.
    # res = ssh('10.2.8.103', cmds=['adb devices', 'adb shell ip addr show wlan0'])
    # # print(type(res))
    # print(re.findall(r'inet (.*?)/', ''.join(res)))
    # all_connect('10.2.9.18')
