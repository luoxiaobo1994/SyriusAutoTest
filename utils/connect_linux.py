# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/1/4 23:36
import time

import paramiko
from utils.log import logger

devices = {}


def ssh(ip, cmds=[], username='syrius', password="syrius", port=22, i=False, timeout=15):
    client = paramiko.SSHClient()
    try:
        # 创建ssh客户端
        # 第一次ssh远程连接时，会提示输入yes或no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 密码方式远程连接
        client.connect(ip, username=username, password=password, timeout=timeout)
        logger.debug(f"{ip}:{port}\t连接成功。")
        # 互信方式远程连接，没用到过，暂时屏蔽了。先保留代码,以后也许会用上.
        # key_file = paramiko.RSAKey.from_private_key_file('输入你的文件路径')
        # ssh.connect(syr_ip)
        out = []  # 返回的结果
        # 执行命令
        if cmds:  # 有时候不执行命令.
            for command in cmds:
                logger.debug(f"执行命令:{command}")
                # 命令的输入和输出流以类似于Python file的对象的形式返回，它们代表stdin，stdout和stderr。
                stdin, stdout, stderr = client.exec_command(command, bufsize=-1,
                                                            timeout=timeout, get_pty=False, environment=None)
                # 读取执行命令后输出的内容
                out = stdout.readlines()  # 不执行输出,有些命令居然执行不成功,妈的.
                if i:  # 控制一下,是否打印消息.
                    for m in out:
                        logger.debug(f"执行命令结果:{m}")
                time.sleep(1)  # 执行一条命令,等待一下,多线程,倒是无所谓了.
        return out
    except Exception as e:
        logger.warning(f"{ip} {e}")
        return 0
    finally:
        client.close()


if __name__ == '__main__':
    # cmds = ["adb devices", "adb tcpip 5555"]
    # cmdss = ['killall navigation_skill',"adb devices", "adb tcpip 5555"]
    cmdss = ['tar xvf /etc/syrius/config_tree.tar.gz']
    # for i in devices.keys():
    for i in devices.keys():
        ssh(ip=i, cmds=[])
