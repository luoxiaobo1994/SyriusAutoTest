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
                out.extend(stdout.readlines())  # 不执行输出,有些命令居然执行不成功,妈的.
                if i:  # 控制一下,是否打印消息.
                    for m in out:
                        logger.debug(f"执行命令结果:{m}")
                time.sleep(1)  # 执行一条命令,等待一下,多线程,倒是无所谓了.
        return 1, out
    except Exception as e:
        logger.warning(f"{ip} {e}")
        return 0
    finally:
        client.close()


def Linux_command(ip, command, index=0, port=22, username='syrius', password='syrius', name='', need=''):
    '''用于执行linux命令，并返回执行结果'''
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, username, password)
        stdin, stdout, stderr = ssh.exec_command(command)
        res = stdout.readline()
        ssh.close()
        if 'No such file or directory' in res:
            return f'机器人:{ip}，执行命令:[{command}]，查询的文件不存在。请注意检查！'
        if res:
            if need and need not in res:
                return f'执行命令:[{command}]，产生的结果与预期不一致，[{need}]不在[{res}]内。'
            return name + res.replace('\n', '') if index else name + res.replace('\n', '')
        else:
            return f'机器人:{ip}，执行命令:[{command}]，没有结果。请注意检查！'

    except Exception as e:
        return e


if __name__ == '__main__':
    cmds = ["adb devices", "adb shell ip addr show wlan0"]
    res = ssh(ip='10.2.9.18', cmds=cmds)
    print(res)
