# -*- coding:utf-8 -*-
# Author: wangkai


import paramiko
from loguru import logger
import re


ssh = paramiko.SSHClient()


# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

def ssh_login(ip, port, username, passwd):
    """
    ssh登录信息
    :param ip:
    :param port:
    :param username:
    :param passwd:
    :return:
    """
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, passwd)
    logger.debug(f"远程IP为：【{ip}】, 端口为：【{str(port)}】, 账号为：【{username}】, 密码为：【{passwd}】")
    return


def ssh_exe_cmd(cmd):
    """
    原始登录信息
    :param cmd:
    :return:
    """
    global ssh
    logger.debug(f"原始指令为：【{cmd}】")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read().decode('utf-8')
    result = result.strip() #删除前后空格
    logger.debug(f"返回结果为：【{result}】")
    return result

def closeSSH():
    #关闭链接，没有单独进行关闭的原因是因为大部分的都属于ssh链接，公用一个链接，使用完毕之后在关闭。避免浪费系统资源
    ssh.close()
    logger.debug("SSH关闭成功！！！")



def movebaseVersion(cmd):
    """
    测试代码：
    获取机器人L4TVendor的构建时间
    buildNum暂时获取不到
    :return:
    """
    robotSystem = ssh_exe_cmd(cmd)
    # print(robotSystem)
    buildTime = re.findall('build date:\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', robotSystem)
    logger.info(f"L4TVendor的构建时间为：【{buildTime[0][11:]}】")


def main():
    # ssh_login('10.2.8.103', 22, 'syrius', 'syrius')
    ssh_login('10.2.16.200', 9524, 'syrius', 'syrius')

    # ssh_exe_cmd('pwd')
    # ssh_exe_cmd('ifconfig')
    movebaseVersion('cat /etc/version.yaml')

    ssh.close()
    return


# main()