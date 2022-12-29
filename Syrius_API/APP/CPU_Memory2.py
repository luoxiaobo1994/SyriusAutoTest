# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/12/28 14:02
# Desc:  从机器人系统获取数据，不好用，TOP的数据不好返回。


import datetime
import re
import time

import paramiko

# 全局数据
ssh = paramiko.SSHClient()  # 连接实例


def pp(msg, level='DEBUG', color='g'):
    if not color:
        # 充当log函数
        print(f"{datetime.datetime.now()} [{level}] : {msg}")
    else:
        if color in ['g', 'green', 'GREEN', 'Green']:
            print(f"\033[1;36m{datetime.datetime.now()} [{level}] : {msg}\033[0m")
        elif color in ['r', 'red', 'RED', 'Red']:
            print(f"\033[1;31m{datetime.datetime.now()} [{level}] : {msg}\033[0m")


def sshLogin(ip='10.2.9.181', port=22, username='developer', passwd='developer'):
    # 连接远程服务
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, port, username, passwd, timeout=5)
        pp(msg=f"开始连接：[{ip}], 端口为：[{str(port)}], 账号为：[{username}], 密码为：[{passwd}]。", color='g')
        pp(f"连接[{ip}]成功。")
    except TimeoutError:
        pp(msg=f"连接{ip}失败，失败原因：超时。", level='WARNING', color='r')
        raise TimeoutError


def exe_cmd(cmd='ls', isreturn=True, printres=False, timeout=3, username='developer', passwd='developer'):
    # 执行命令。只包含命令和是否返回结果两个参数，具体业务，再分函数细写。
    global ssh
    # pp(f"执行命令：{cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True, timeout=timeout)  # get_pty参数，是为了sudo命令输入密码使用的。
    result = stdout.read().decode('utf-8')
    result = result.strip()  # 删除前后空格
    result.replace('\n', '')
    if cmd.startswith('sudo'):
        stdin.write(passwd + '\n')
        time.sleep(0.5)
        stdin.flush()
    if 'Permission denied' in result:
        pp(f'执行命令：{cmd}的权限不够，请检查。', 'WARNING', color='r')
    if isreturn:
        if printres:
            pp(f"命令的返回结果：{result}", 'DEBUG', color='r')
        return result


def sshClose():
    # 关闭远程连接。
    global ssh
    ssh.close()
    pp(f"操作完毕，关闭ssh连接。", color='g')
    pp('*-' * 20)


def getinfo():
    pp('开始执行业务')
    res = exe_cmd('adb shell top')  # 这个数据不能正常返回。
    pp(res)


def main():
    sshLogin()
    getinfo()
    sshClose()


if __name__ == '__main__':
    main()
