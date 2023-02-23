# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/1/5 11:14
import time

import paramiko
import scp

from utils.log import logger


def scp_file(device, file, path, port=22, username='developer', password='developer', commands=[], get_result=False):
    ssh_client = paramiko.SSHClient()
    logger.debug(f"开始连接：[{device}], 端口为：[{str(port)}], 账号为：[{username}], 密码为：[{password}]。")
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    try:
        ssh_client.connect(device, port=port, username=username, password=password, timeout=15)
    except TimeoutError:
        logger.warning(f"连接[{device}]超时，请检查是否能正常连接该设备。")
        return
    scp_client = scp.SCPClient(ssh_client.get_transport(), socket_timeout=15)
    try:
        scp_client.put(files=file, remote_path=path)
    except FileNotFoundError as e:
        logger.error(f"找不到传输的文件，请检查。{e}:{file}")
    else:
        logger.debug(f"文件：[{file}]成功传输到设备[{device}]的[{path}]目录下成功。")
    if commands:  # 传完之后，还需要做一些操作，如：查看大小，修改权限之类的。
        for cmd in commands:
            stdin, stdout, stderr = ssh_client.exec_command(cmd, get_pty=True)
            logger.debug(f"执行命令: '{cmd}' 完成")
            if get_result:
                result = stdout.read().decode('utf-8').strip()  # 返回的结果
                if result:
                    logger.debug(f"命令的返回值：'{result}'")
                else:
                    logger.debug(f"该命令没有返回值。")
                time.sleep(0.3)
        logger.debug("执行完成所有命令。")
    ssh_client.close()


if __name__ == '__main__':
    def main():
        # 机器人IP清单，如有分组，不同组传不同配置，则分组写入机器人IP。 或者集中在一起也可。
        robots = ['10.2.9.181', '10.2.8.103']  # 机器人IP，用列表和字典或集合都行，只要循环取到IP即可。
        file = "./log.py"  # 需要传输的文件，填好绝对/相对路径。
        path = '~/'  # 需要传到目标机器人的哪个目录下
        for bot in robots:  # 循环遍历列表传送即可。
            scp_file(device=bot, file=file, path=path, commands=['chmod 777 ~/log.py', 'ls -lh ~/log.py'])
            logger.debug(f"机器人[{bot}]执行完成。\n")


    main()
