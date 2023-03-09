# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/12/1 10:45
# Desc: 测试前检查机器人测试环境信息。

import datetime
import re
import time
import os
import paramiko
import pytz

# 全局数据
ssh = paramiko.SSHClient()  # 连接实例


def pp(msg, level='DEBUG', color='g'):
    file = 'D:\checkLog\check_log.txt'
    if not os.path.exists(file):
        file = './check_log.txt'  # 如果没有，就在当前目录创建日志文件。
    with open(file, 'a') as f:
        f.write(f"{datetime.datetime.now()} [{level}] : {msg}\n")
    if color in ['g', 'green', 'GREEN', 'Green']:
        print(f"\033[1;36m{datetime.datetime.now()} [{level}] : {msg}\033[0m")
    elif color in ['r', 'red', 'RED', 'Red']:
        print(f"\033[1;31m{datetime.datetime.now()} [{level}] : {msg}\033[0m")


def time_difference(time1, time2):
    try:
        t1 = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
        t2 = datetime.datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')
        if t1 < t2:  # 两个都是字符串，直接比较。
            return [(t2 - t1).days, (t2 - t1).seconds]  # 返回天和秒。
        return [(t1 - t2).days, (t1 - t2).seconds]
    except:
        pp(f"时间比较函数，传入参数异常，传入格式为：'%Y-%m-%d %H:%M:%S'，如：'2023-02-06 03:10:39'", "WARNING", color='r')


def sshLogin(ip, port, username='developer', passwd='developer'):
    # 连接远程服务
    global ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, port, username, passwd, timeout=5)
        pp(msg=f"开始连接：[{ip}], 端口为：[{str(port)}], 账号为：[{username}], 密码为：[{passwd}]。")
        pp(f"连接[{ip}]成功。")
    except TimeoutError:
        pp(msg=f"连接{ip}失败，失败原因：超时。", level='WARNING', color='r')
        # raise TimeoutError


def exe_cmd(cmd='ls', isreturn=True, printres=False, timeout=3, username='developer', passwd='developer'):
    # 执行命令。只包含命令和是否返回结果两个参数，具体业务，再分函数细写。
    global ssh
    # pp(f"执行的命令：{cmd}")  # , get_pty=True, timeout=timeout
    stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True, timeout=timeout)  # get_pty参数，是为了sudo命令输入密码使用的。
    if cmd.startswith('sudo'):
        pp(f'执行的命令带有sudo，写入用户密码...')
        stdin.write(passwd + '\n')
        time.sleep(1)
        stdin.flush()
    result = stdout.read().decode('utf-8')
    result = result.strip()  # 删除前后空格
    result.replace('\n', '')
    if 'Permission denied' in result:
        pp(f'执行命令：{cmd}的权限不够，请检查。', 'WARNING', color='r')
    if isreturn:
        if printres:
            pp(f"命令的返回结果：{result}")
        return result


def sshClose():
    # 关闭远程连接。
    global ssh
    ssh.close()
    pp(f"操作完毕，关闭ssh连接。")
    pp('*-' * 20 + '\n')


# 以下是具体业务函数。-----------------------------------------------------------------
def basic_info():
    # 检查MoveBase版本
    MoveBase = exe_cmd('cat /opt/cosmos/etc/ota/version')
    pp(f'MoveBase版本：{MoveBase}')
    # 检查L4T信息
    L4T_date = exe_cmd("grep -E 'build date:(.*?)$' /etc/version.yaml")
    L4t_version = exe_cmd('cat /etc/jurassic_release')
    if L4t_version:
        pp(f"L4T构建日期：{L4T_date}，版本：{L4t_version}")
    else:
        pp(f"L4T构建日期：{L4T_date}。")
    # 检查SN
    SN = exe_cmd('cat /sys/robotInfo/RobotSN')
    SN = SN.split()[0]  # 直接替换换行符有点问题。
    pp(f"机器人的SN：{SN}")
    # 检查ID
    ID_res = exe_cmd('dbus-send --system --print-reply=literal --type=method_call --dest=com.'
                     'syriusrobotics.secbot /buzzard/secbot com.syriusrobotics.secbot.ISecBot.getDroidId')
    ID = ID_res.split()[0]
    if ID == 'Error' or len(ID) <= 30:  # 长度是32的数字字母组合，如：747cd6f5d33e4c1cac045de78852c79d
        pp(f"机器人的ID异常，请检查一下，拿到的值：{ID}", "WARNING", color='r')  # 去掉  int32 0
    else:
        pp(f"机器人的ID：{ID}")
    # 检查Java进程数量
    java_process = exe_cmd('ps -aux | grep java | wc -l')
    if int(java_process) >= 10:
        pp(f"Java进程数量：{java_process}，{'正常。'}")
    else:
        pp(f"Java进程数量：{java_process}，{'不正常。'}", "WARNING", color='r')


def calibration():
    # 标定文件检查。
    detail = exe_cmd("sudo grep -E 'Sensors:' /opt/cosmos/etc/calib/calibration_result/robot_sensors.yaml")
    # pp(f"res:{res}")
    file_size = exe_cmd("ls -lh /opt/cosmos/etc/calib/calibration_result/robot_sensors.yaml").split()[4]
    # pp(f"res2:{res2}")
    if 'No such file or directory' in detail:
        pp(f"机器人的标定文件检查异常，文件不存在。", level='WARNING', color='r')
    elif 'Permission denied' in detail:
        pp(f"无权限查看标定文件。标定文件的大小是：{file_size}")
    elif 'Sensors:' in detail and file_size != '0':
        if file_size > '3':
            pp(f"机器人的标定文件正常。标定文件大小：{file_size}")
        else:
            pp(f"标定文件大小有异常：{file_size}", level='WARNING', color='r')
    else:
        pp(f"机器人的标定文件检查异常，脚本未查询到相关数据，请手动检查。", level='WARNING', color='r')
    carrier = exe_cmd("cat /opt/cosmos/data/robot/storage.yaml").replace('\r\n', '，')
    carrier_size = re.findall('\d{1,2}\.', carrier)
    if 'No such file or directory' in carrier:
        pp(f"载具信息：{carrier}", 'WARNING', 'R')
    else:
        pp(f"载具信息：{carrier}")


def check_time(repair=True):
    # 先检查是否开启了时钟同步功能。
    is_time_sync = exe_cmd("sudo systemctl is-active systemd-timesyncd").split('\r\n')
    if 'inactive' in is_time_sync:
        pp(f"当前机器人时钟同步进程未开启：{is_time_sync[-1]}，有严重运行风险，请检查！！！", 'WARNING', 'r')
    else:
        pp(f"当前机器人时钟同步进程为激活状态：{is_time_sync[-1]}，开始检查时钟同步情况。")
    # 检查机器人时间
    robot_time = exe_cmd("date +'%Y-%m-%d %H:%M:%S'")
    utc_time = datetime.datetime.now(pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S')  # '2023-02-06 03:10:39'
    pp(f"机器人时间：{robot_time}，UTC—0时间：{utc_time}")  # 拿到的时间：2023-02-06 03:05:10
    time_gap = time_difference(robot_time, utc_time)  # 机器人时间与当前UTC0时间差距。
    if time_gap[-1] > 10:
        pp(f"机器人当前时间：{robot_time}，与本机的时间差(UTC+0)是：{time_gap[0]}天{time_gap[-1]}秒。", 'WARNING',
           color='r')
        pp(f"机器人当前时间与实际UTC时间差距较大，请检查！", "WARNING", color='r')
    else:
        pp(f"机器人当前时间：{robot_time}，与本机的时间差(UTC+0)是：{time_gap[-1]}秒。")
    pad_robot_timestamp = ''
    date_command = "adb shell date +%s%3N && date +%s%3N"
    try:
        pad_robot_timestamp = exe_cmd(date_command).split()
        if pad_robot_timestamp[0][-2:] == '3N':  # 安卓版本的时间戳获取会异常，3N不能正常转化。
            pad_timestamp = pad_robot_timestamp[0].replace('3N', '')  #
            robot_timestamp = pad_robot_timestamp[1][:len(pad_timestamp)]
            time_diff = abs(int(pad_timestamp) - int(robot_timestamp))  # 这种情况下，拿到的时间差是秒。
            if time_diff >= 2:
                pp(f"上下位机的时间戳相差超过2s，请检查一下。", level='WARNING', color='r')
            else:
                pp(f"上下位机的时间戳相差为：{time_diff}秒。")
        else:
            time_diff = abs(int(pad_robot_timestamp[0]) - int(pad_robot_timestamp[1]))  # 这种情况下，拿到的时间差是毫秒。
            if time_diff > 2000:
                pp(f"上下位机的时间戳相差超过2s，请检查一下。", level='WARNING', color='r')
            else:
                pp(f"上下位机的时间戳相差为：{time_diff}毫秒。")
    except Exception as e:
        pp(f"获取时间命令：{date_command}返回结果异常，请检查：{pad_robot_timestamp}。异常类型：{e}。", "WARNING", 'r')


def check_time_sync():
    while True:
        is_time_sync = exe_cmd("sudo systemctl is-active systemd-timesyncd").split('\r\n')
        if 'inactive' in is_time_sync:
            pp(f"当前机器人时钟同步进程未开启：{is_time_sync[-1]}，有严重运行风险，请检查！！！", 'WARNING', 'r')
        else:
            pp(f"当前机器人时钟同步进程为激活状态：{is_time_sync[-1]}，注意检查时钟同步情况。")
        time.sleep(10)


def diskUsage():
    # 检查磁盘占用率
    res = exe_cmd('df | head -2 | grep /')  # 总磁盘占用率。
    res2 = exe_cmd('df -h | grep "[0-9]\?[0-9]\?[0-9]%" -o').split('\r\n')  # 查找出所有目录的磁盘占用率,处理成列表
    total_percent = re.findall('\d+%', res)[0]
    threshold = '85%'
    if total_percent > threshold:
        pp(f"机器人的磁盘占用大于{threshold}，执行:1.日志清除命令。2.删除home目录下的更新包", "WARNING", color='r')
        exe_cmd('sudo journalctl --vacuum-size=1K')
        exe_cmd('rm -rf ./update_*')
    for percent in res2:
        if percent > "90%":  # 90% 做门限值。
            pp(f"有目录占用率达到{percent}，可能影响功能使用，请检查。", "WARNING", color='r')
            pp(f"目录信息：{exe_cmd(f'df -h | grep {percent}')}")
    else:
        pp(f"机器人磁盘占用空间正常，当前占用：{total_percent}")


def clearOTA():
    # 清除OTA下载缓存
    exe_cmd('rm -rf /opt/syrius/cache/ota_client/downloader/*')
    exe_cmd('rm -rf /opt/syrius/cache/ota_client/facade/*')
    pp("清除OTA缓存。")


def env(ip, port='22', count=3):
    res1 = exe_cmd('cat /opt/cosmos/bin/ota/checker/application.yml')
    res2 = exe_cmd('cat /opt/cosmos/bin/iot-gateway/application.yml')
    res3 = exe_cmd('cat /opt/cosmos/bin/secbot/application.yml')
    if 'env: test' in res1 and res1 == res2 == res3:
        pp(f"机器人的环境为：{res1}")
    else:
        pp(f"机器人的环境文件缺失，使用echo创建测试环境配置文件。", "WARNING", color='r')
        try:
            exe_cmd("echo 'env: test' > /opt/cosmos/bin/secbot/application.yml")
            exe_cmd("echo 'env: test' > /opt/cosmos/bin/iot-gateway/application.yml")
            exe_cmd("echo 'env: test' > /opt/cosmos/bin/ota/checker/application.yml")
            pp(f"环境配置文件创建完成。")
        except TimeoutError:
            pp(f"环境配置文件创建失败，请检查。", "WARNING", color='r')


def skill_file():
    res1 = set(exe_cmd('ls /opt/cosmos/bin').split())
    skill = {'bootstrapper', 'jinglebell', 'ota', 'share', 'calibration_skill', 'keyring', 'oxe', 'time_sync',
             'cpu_mem_monitor.sh', 'kuafu', 'psyche', 'tx2_web_server', 'gadgetman', 'lost+found', 'pulseaudioman',
             'video_device.sh', 'health_skill', 'maintenance', 'README.txt', 'inuitive_xusb_detector', 'mapping_skill',
             'scanner_skill', 'iot-gateway', 'navigation_skill', 'secbot', 'cleaning_skill'}
    if res1.difference(skill):
        pp(f"/opt/cosmos/bin目录下的文件检查有差异，差异项：{res1.difference(skill)}", "WARNING", color='r')
    else:
        pp(f"/opt/cosmos/bin目录下的文件检查:正常。")


def iot():
    res1 = set(exe_cmd('ls /opt/cosmos/bin/iot-gateway').split())
    file = {'iot-gateway', 'iot-gateway.sh', 'application.yml', 'stop.sh'}
    if res1 & file != file:
        pp(f"/opt/cosmos/bin/iot-gateway目录下的文件缺失，检查到的结果：{res1}", "WARNING", color='r')
    else:
        pp(f"/opt/cosmos/bin/iot-gateway目录下的文件检查:正常。")
        for i in res1:
            if 'iot-gateway' in i and '.jar' in i:
                pp(f"当前机器人的iot-gateway版本是：{i}")


def kuafu_file():
    res1 = set(exe_cmd('ls /opt/cosmos/bin/kuafu').split())
    file = {'run.sh'}
    if res1 & file != file:
        pp(f"/opt/cosmos/bin/kuafu目录下的文件缺失，检查到的结果：{res1}", "WARNING", color='r')
    else:
        pp(f"/opt/cosmos/bin/kuafu目录下的文件检查:正常。")
        for i in res1:
            if 'kuafu_gateway_classic' in i and '.jar' in i:
                pp(f"当前机器人的kuafu_gateway_classic版本是：{i}")


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
        'LMLBA0100': '重龙PA版样机',
    }
    try:
        res = exe_cmd('cat /sys/robotInfo/Model')[:9]
        res2 = exe_cmd('cat /opt/cosmos/etc/ota/model')
        if model.get(res):
            pp(f"机器人Model是：{res}，机型名称：{res2}，对应机型：{model[res]}")
        else:
            pp(f"机器人Model是：{res}，没有对应机型，请检查。", "WARNING", color='r')
    except TypeError:
        pp(f"机器人Model查询结果返回异常，请检查。", "WARNING", color='r')


def user_color():
    res = exe_cmd("grep -E 'force_color_prompt=yes' .bashrc")
    if '#' in res:
        exe_cmd("sed -i 's/#force_color_prompt=yes/force_color_prompt=yes/g' .bashrc")
        exe_cmd("source .bashrc")
        pp(f"用户颜色未生效，修改同步完成。", "WARNING", color='r')
    else:
        pp(f"用户颜色已生效，未做修改。")


def startAgent():
    pass


def debug():
    pass
    # res = exe_cmd("sudo systemctl is-active systemd-timesyncd").split('\r\n')
    # pp(f"res:{res}")


def main(ip='10.2.16.200', port=22):
    try:
        sshLogin(ip=ip, port=port, username='developer', passwd='developer')
        basic_info()
        calibration()
        check_time()
        diskUsage()
        model()
        env(ip=ip)
        skill_file()
        kuafu_file()
        iot()
        user_color()
        # debug()
        sshClose()
    except Exception as e:
        pp(f"发生了一些异常：{e}", level='ERROR', color='r')  # 登录函数会自己打印异常消息。其他异常，需要刷一下。


if __name__ == '__main__':
    robot = {
        '雷龙·苏亚雷斯': '10.2.9.181',
        '雷龙·内马尔': '10.2.8.255',
        '雷龙·布里茨': '10.2.9.125',
        '雷龙·C罗': '10.2.8.118',
        '梁龙·鸣人': '10.2.8.103',
        '网卡211': '10.2.8.211',
        '梁龙·佐助': '10.2.8.77',
        '网卡82': '10.2.9.82',
        '网卡242': '10.2.8.242',
    }
    # main(robot['雷龙·苏亚雷斯'])
    # main(robot['雷龙·内马尔'])
    main(robot['雷龙·布里茨'])
    # main(robot['雷龙·C罗'])
    # main(robot['梁龙·鸣人'])
    # main(robot['网卡211'])
    # main(robot['网卡82'])
    # main(robot['网卡242'])
    # main(robot['梁龙·佐助'])
    # main('10.2.9.39')  # 重龙PA版样机。
