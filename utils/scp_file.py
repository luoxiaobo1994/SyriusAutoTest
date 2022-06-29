# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/1/5 11:14

import paramiko
import scp

from utils.log import logger


def scp_navi(device, file, path, port=22, username='syrius', password='syrius', setup_cmd='ls', commands=[]):
    ssh_client = paramiko.SSHClient()
    logger.debug(f"开始连接：{device}...")
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh_client.connect(device, port=port, username=username, password=password)
    scp_client = scp.SCPClient(ssh_client.get_transport(), socket_timeout=15)
    ssh_client.exec_command(command=setup_cmd, bufsize=-1, timeout=60, get_pty=False,
                            environment=None)
    try:
        scp_client.put(files=file, remote_path=path)
    except FileNotFoundError as e:
        logger.error(f"{e}:{file}")
    else:
        logger.debug(f"文件：{file} 传输到{device}的路径：{path}成功。")
    if commands:
        for cmd in commands:
            stdin, stdout, stderr = ssh_client.exec_command(cmd, bufsize=-1, timeout=60, get_pty=False,
                                                            environment=None)
            logger.debug(f"执行命令: {cmd} 完成")
            logger.debug(f"执行结果:{stdout.readlines()[:5]}")  # 前五行就行了.
        logger.debug("执行完成命令。")
    ssh_client.close()


if __name__ == '__main__':
    def xx():
        devices_A = ['10.111.150.216', '10.111.150.193', '10.111.150.204', '10.111.150.205', '10.111.150.211',
                     '10.111.150.210', '10.111.150.201', '10.111.150.206', '10.111.150.214', '10.111.150.213']
        devices_B = ['10.111.150.203', '10.111.150.104', '10.111.150.209', '10.111.150.102', '10.111.150.106',
                     '10.111.150.195', '10.111.150.202', '10.111.150.212']
        devices_C = ['10.111.150.215', '10.111.150.111', '10.111.150.108', '10.111.150.125', '10.111.150.121',
                     '10.111.150.117', '10.111.150.207', '10.111.150.208']
        all_devices = devices_A + devices_B + devices_C
        # 命令执行前,注意加路径.
        # command_ls = ['chmod 755 /usr/local/bin/navigation_skill', 'killall navigation_skill']
        command_ls = ['tar xvf /etc/syriusconfig_tree.tar.gz']
        rm_file = 'rm -rf /etc/syrius/config_tree'  # 删除原有的文件。
        for device in devices_C:
            try:
                scp_navi(device=device, file=r"C:\Users\luoxiaobo\111.txt",
                         path="/etc/syrius/offline_map/map_01/common/",
                         commands=[])
            except Exception as e:
                print(e)


    xx()
