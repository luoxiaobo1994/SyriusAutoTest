import re
import sys

from loguru import logger

from com.syrius.util.sshUtil import ssh_login, closeSSH, ssh_exe_cmd

logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
logger.add(sys.stderr, level="DEBUG")  # level=TRACE,DEBUG,INFO,SUCCESS,WARNING,ERROR,CRITICAL


# 使用脚本测试时，建议使用ERROR，调试脚本时使用DEBUG


def checker_system_services(checker_map):
    command = "systemctl list-unit-files"
    result = ssh_exe_cmd(command)
    result_array = re.split("\\n", result)[:-2]  # 去除最后两行无关数据
    for key, value in checker_map.items():
        flage_exist = False
        for one_line in result_array:
            key_values_list = re.split("[ ]{1,}", one_line)
            if key == key_values_list[0]:
                flage_exist = True
                if value == key_values_list[1]:
                    logger.info(f"系统进程中包含进程：【{key_values_list[0]}:{key_values_list[1]}】")
                else:
                    logger.error(f"系统进程中期望值为：【{key}:{value}】，实际结果为：【{key_values_list[0]}:{key_values_list[1]}】")

        if flage_exist is False:
            logger.error(f"系统进程中不包含有进程：【{key}:{value}】")


def main(addr, checker_map):
    '''  登录信息拼接，开启链接 '''
    address = addr.split(":")
    ssh_login(address[0], address[1], "developer", "developer")

    ''' 获取对应的信息 '''
    checker_system_services(checker_map)

    ''' 关闭链接 '''
    closeSSH()


if __name__ == '__main__':
    # 所有机器信息
    robotMap = {
        '雷龙-齐达内': '10.2.8.65:22',
        '雷龙-内马尔': '10.2.8.57:22',
        '雷龙-苏亚雷斯': '10.2.9.181:22',
        '梁龙-佐助': '10.2.8.103:22',
        '梁龙2-索隆': '10.2.8.211:22',
        '电子平台1-无外网': '10.2.8.193:22',
        '电子平台1-有外网': '10.2.16.200:9542'
    }

    # 待检查的服务列表
    checker_map = {
        'handle_robotic_amixer_settings.service': 'enabled',
        'handle_robotic_can_bus_enable.service': 'enabled',
        'buzzard_ota.service': 'enabled',
        'buzzard_permission_define.service': 'enabled',
        'syrius-boot-sound.service': 'enabled',
        'syrius-net-player.service': 'enabled',
        'syrius-psyche.service': 'enabled'
    }
    main(robotMap['电子平台1-有外网'], checker_map)
