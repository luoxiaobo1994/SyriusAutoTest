# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/2/22 11:30
# Desc:  优化连接linux脚本。

import time
import paramiko
import scp
from utils.mylog import Logger
from atexit import register


class MySSH:

    def __init__(self, ip, port=22, username='developer', password='developer', logfile='ssh_log.txt', timeout=5):
        self.log = Logger(logfile)
        self.username = username
        self.password = password
        self.device = ip
        register(self.del_func)
        # 连接远程服务
        global ssh
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(ip, port, username, password, timeout=timeout)
            self.log.debug(f"开始连接：[{ip}], 端口为：[{str(port)}], 账号为：[{username}], 密码为：[{password}]。")
            self.log.debug(f"连接[{ip}]成功。")
        except TimeoutError:
            self.log.warning(f"连接{ip}失败，失败原因：超时。")

    def exe_cmd(self, cmd='ls', isreturn=True, printres=False, timeout=15):  # adb 等待时间较长，多给点超时时间。
        # 执行命令。只包含命令和是否返回结果两个参数，具体业务，再分函数细写。
        # get_pty参数，是为了sudo命令输入密码使用的。
        self.log.debug(f"执行命令：'{cmd}'")
        stdin, stdout, stderr = self.ssh.exec_command(cmd, get_pty=True, timeout=timeout)
        if cmd.startswith('sudo'):
            self.log.debug(f'执行的命令带有sudo，写入用户密码...')
            stdin.write(self.password + '\n')
            time.sleep(1)
            stdin.flush()
        result = stdout.read().decode('utf-8')
        result = result.strip()  # 删除前后空格
        result.replace('\n', '')
        if 'No such file or directory' in ''.join(result):
            self.log.warning(f"注意：命令操作的对象不存在。")
            return 0
        if 'command not found' in ''.join(result):
            self.log.warning(f"注意：命令输入有误，或者执行异常！sehll返回：command not found")
            return 0
        if 'Permission denied' in result:
            self.log.warning(f'执行命令：{cmd}的权限不够，请检查。')
            return 0
        if isreturn:
            if printres:
                self.log.debug(f"命令的返回结果：{result}")
            return result

    def scp_file(self, file, path):
        # 传输文件。
        scp_client = scp.SCPClient(self.ssh.get_transport(), socket_timeout=15)
        try:
            self.log.debug(f"开始向：[{self.device}]的目录：[{path}]传输文件：[{file}]。请等待。。。")
            scp_client.put(files=file, remote_path=path)
        except FileNotFoundError as e:
            self.log.error(f"找不到传输的文件，请检查。{e}:{file}")
            return
        else:
            self.log.debug(f"传输文件：[{file}]到设备[{self.device}]的[{path}]目录--成功。")
        time.sleep(1)

    def del_func(self):
        # 关闭远程连接。
        self.log.debug(f"操作完毕，关闭ssh连接。")
        self.log.debug('*-' * 20 + '\n')
        self.ssh.close()



if __name__ == '__main__':
    robots = {
        '雷龙·苏亚雷斯': '10.2.9.181',
        '雷龙·内马尔': '10.2.8.255',
        '雷龙·布里茨': '10.2.9.125',
        '雷龙·C罗': '10.2.8.118',
        '梁龙·鸣人': '10.2.8.103',
        '网卡211': '10.2.8.211',
        '梁龙·佐助': '10.2.8.77',
        '网卡82': '10.2.9.82',
    }

    ssh = MySSH(ip=robots['雷龙·内马尔'])
    ssh.scp_file(r"E:\工作\测试资料\ServerAgent-2.2.3.zip", './')
    ssh.exe_cmd('unzip ServerAgent-2.2.3.zip')
    ssh.exe_cmd('chmod +x ServerAgent-2.2.3/startAgent.sh')
    time.sleep(1)
    ssh.exe_cmd('./ServerAgent-2.2.3/startAgent.sh &')
