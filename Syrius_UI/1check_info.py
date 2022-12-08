# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/12/1 10:45
# Desc: 测试前检查机器人测试环境信息。

import datetime
import re
import time

import paramiko

# 全局数据
ssh = paramiko.SSHClient()  # 连接实例
# 现有机器人列表。
robot = {
    '苏亚雷斯': '10.2.9.181',
    '齐达内': '10.2.8.65',
    '内马尔': '10.2.8.57',
    '鸣人': '10.2.8.130'
}


def pp(msg, level='DEBUG'):
    # 充当log函数
    print(f"{datetime.datetime.now()} [{level}] : {msg}")


def sshLogin(ip, port, username='factory', passwd='factory'):
    # 连接远程服务
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, port, username, passwd, timeout=10)
        pp(msg=f"开始连接：[{ip}], 端口为：[{str(port)}], 账号为：[{username}], 密码为：[{passwd}]。")
        pp(f"连接[{ip}]成功。")
    except TimeoutError:
        pp(msg=f"连接[]失败，失败原因：超时。", level='WARNING')


def exe_cmd(cmd='ls', isreturn=True, printres=False, timeout=3, username='factory', passwd='factory'):
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
        pp(f'执行命令：{cmd}的权限不够，请检查。', 'WARNING')
    if isreturn:
        if printres:
            pp(f"命令的返回结果：{result}", 'DEBUG')
        return result


def sshClose():
    # 关闭远程连接。
    global ssh
    ssh.close()
    pp(f"操作完毕，关闭ssh连接。")
    pp('*-' * 40)


# 以下是具体业务函数。-----------------------------------------------------------------
def basic_info():
    # 检查MoveBase版本
    MoveBase = exe_cmd('cat /opt/cosmos/etc/ota/version')
    pp(f'MoveBase版本：{MoveBase}')
    # 检查L4T信息
    L4T = exe_cmd("grep -E 'build date:(.*?)$' /etc/version.yaml")
    pp(f"L4T信息：{L4T}")
    # 检查SN
    SN = exe_cmd('cat /sys/robotInfo/RobotSN')
    SN = SN.split()[0]  # 直接替换换行符有点问题。
    pp(f"机器人的SN：{SN}")
    # 检查ID
    ID = exe_cmd('dbus-send --system --print-reply=literal --type=method_call --dest=com.'
                 'syriusrobotics.secbot /buzzard/secbot com.syriusrobotics.secbot.ISecBot.getDroidId')
    pp(f"机器人的ID：{ID.split()[0]}")  # 去掉  int32 0
    # 检查Java进程数量
    java_process = exe_cmd('ps -aux | grep java | wc -l')
    pp(f"Java进程数量：{java_process}，{'正常。' if java_process >= '10' else '数量异常，请检查！'}")


def calibartion():
    # 标定文件检查。
    res = exe_cmd("grep -E 'Sensors:' /opt/cosmos/etc/calib/calibration_result/robot_sensors.yaml")
    res2 = exe_cmd("ls -lh /opt/cosmos/etc/calib/calibration_result/robot_sensors.yaml").split()[4]
    if res and res2:
        pp(f"机器人的标定文件正常。")
    else:
        pp(f"机器人的标定文件检查异常，文件不存在或为空。")


def check_time(repair=True):
    # 检查机器人时间
    res = exe_cmd("date +'%Y-%m-%d %H:%M:%S'")
    pp(f"机器人当前时间：{res}")
    now = str(datetime.datetime.now())
    if res[:10] != now[:10]:
        pp(f"机器人当前时间与实际UTC时间差距较大，请检查！", "WARNING")
        now1 = list(time.localtime())
        date = ''.join([str(i) for i in now1[:3]])
        h = now1[3] - 8  # 基本是上班时间才会去检查。所以减8没问题。半夜做，就有BUG。
        m = now1[4]
        s = now1[5]
        writetime = date + ' ' + ':'.join([str(h), str(m), str(s)])
        # print(writetime)
        if repair:
            pp(f"脚本即将设置时间到当前时间:{writetime}，时间时区为UTC0。")
            exe_cmd(f'sudo date -s "{writetime}"')

    else:
        return 1


def diskUsage():
    # 检查磁盘占用率
    res = exe_cmd('df | head -2 | grep /')
    percent = re.findall('\d+%', res)[0]
    threshold = '85%'
    if percent > threshold:
        pp(f"机器人的磁盘占用大于{threshold}，执行:1.日志清除命令。2.删除home目录下的更新包")
        exe_cmd('sudo journalctl --vacuum-size=1K')
        exe_cmd('rm -rf ./update_*')


def clearOTA():
    # 清除OTA下载缓存
    exe_cmd('rm -rf /opt/syrius/cache/ota_client/downloader/*')
    exe_cmd('rm -rf /opt/syrius/cache/ota_client/facade/*')
    pp("清除OTA缓存。")


def env(count=3):
    res1 = exe_cmd('cat /opt/cosmos/bin/ota/checker/application.yml')
    res2 = exe_cmd('cat /opt/cosmos/bin/iot-gateway/application.yml')
    res3 = exe_cmd('cat /opt/cosmos/bin/secbot/application.yml')
    if 'env: test' in res1 and res1 == res2 == res3:
        pp(f"机器人的环境为：{res1}")
    else:
        pp(f"机器人的环境文件缺失，手动添加配置文件。")
        try:
            cmd1 = 'sudo echo env: test > /opt/cosmos/bin/ota/checker/application.yml'
            cmd2 = 'sudo echo env: test > /opt/cosmos/bin/iot-gateway/application.yml'
            cmd3 = 'sudo echo env: test > /opt/cosmos/bin/secbot/application.yml'
            exe_cmd(cmd1, printres=True)
            exe_cmd(cmd2)
            exe_cmd(cmd3)
        except TimeoutError:
            pp(f"写环境文件命令超时，请检查。")


def model():
    model = {
        'LLLBR0200': '雷龙',  # 非正常添加，手动写的
        'LLLPO0100': '波塞冬',
        'LMLDI0100': '矮版梁龙-雅滕电机',
        'LMLDI0200': '矮版梁龙-自研电机',
        'LMLDI0101': '高版梁龙-雅滕电机',
        'LMLDI0201': '高版梁龙-雅滕电机',
        'LMLDI0400': '矮版梁龙2-雅滕电机-认证',
        'LMLDI0401': '高版梁龙2-雅滕电机-认证',
        'LMLDI0500': '高版梁龙2-雅滕电机-非认证',
        'LMLDI0501': '高版梁龙2-雅滕电机-非认证',
    }
    try:
        res = exe_cmd('cat /sys/robotInfo/Model')[:9]
        pp(f"机器人Model是：{res}，对应机型：{model[res] if model.get(res) else '没有对应机型，请检查。'}")
    except TypeError:
        pp(f"机器人Model查询结果返回异常，请检查。")


def debug():
    exe_cmd('sudo ls')


def main(ip='10.2.16.200',port=22):
    sshLogin(ip, port, 'developer', 'developer')
    basic_info()
    calibartion()
    # check_time()
    # diskUsage()
    # model()
    # env()
    # debug()
    sshClose()


if __name__ == '__main__':
    robot = {
        '雷龙·苏亚雷斯':'10.2.9.181',
        '雷龙·内马尔':'10.2.8.255',
        '雷龙·齐达内': '10.2.8.65',
        '雷龙·C罗': '10.2.8.118',
        '梁龙·鸣人':'10.2.8.103',
        '梁龙·索隆':'10.2.8.211',
        '梁龙·佐助':'10.2.8.77',
    }
    main('雷龙·苏亚雷斯')
    # main('雷龙·内马尔')
    # main('雷龙·齐达内')
    # main('雷龙·C罗')
    # main('梁龙·鸣人')
    # main('梁龙·佐助')
    # main('梁龙·索隆')
