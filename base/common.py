# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2020/11/30 12:00
import csv
import itertools
import os
import random
import socket
import string
import sys
import threading
import time
import traceback
from collections.abc import Iterable
from datetime import datetime

import wcwidth
import yaml

from utils.log import logger

"""
封装一些基础方法,公共使用.
"""


# 时间戳
def get_time():
    now_time = time.localtime()  # [2020, 11, 30, 12, 3, 5, 0, 335, 0]
    date_1 = '-'.join(str(i).zfill(2) for i in now_time[:3])
    time_1 = ':'.join(str(i).zfill(2) for i in now_time[3:6])
    return date_1 + ' ' + time_1 + ' '


def file_time():
    now_time = time.localtime()  # [2020, 11, 30, 12, 3, 5, 0, 335, 0]
    date_1 = '-'.join(str(i).zfill(2) for i in now_time[:3])
    time_1 = '-'.join(str(i).zfill(2) for i in now_time[3:6])
    return date_1 + '_' + time_1


# 也是时间戳,不带日期,只有时分秒的.
def get_timer():
    now_time = time.localtime()  # [2020, 11, 30, 12, 3, 5, 0, 335, 0]
    time_1 = ':'.join(str(i).zfill(2) for i in now_time[3:6])
    return time_1


# 获取日期，用于创建文件名
def get_date():
    now_time = time.localtime()  # [2020, 11, 30, 12, 3, 5, 0, 335, 0]
    date_1 = '-'.join(str(i).zfill(2) for i in now_time[:3])
    return date_1


def time_difference(time1, time2):
    try:
        t1 = datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
        t2 = datetime.strptime(time2, '%Y-%m-%d %H:%M:%S')
        if t1 < t2:  # 两个都是字符串，直接比较。
            return [(t2 - t1).days, (t2 - t1).seconds]  # 返回天和秒。
        return [(t1 - t2).days, (t1 - t2).seconds]
    except:
        pp(f"时间比较函数，传入参数异常，传入格式为：'%Y-%m-%d %H:%M:%S'，如：'2023-02-06 03:10:39'", "WARNING", color='r')


# 调试打印,带时间戳
def dp(*args):
    print(get_time(), *args)


def get_file():
    # return __file__
    return os.path.split(__file__)[1].split('.')[0]


# 冒泡排序
def bubble_sort(nums):
    for i in range(len(nums) - 1):  # 控制循环次数
        flag = False  # 优化点2,交换标志,产生交换,则为真.某次循环,没有产生交换.则说明序列已经有序.跳出循环了.
        for j in range(len(nums) - i - 1):  # 优化点1,控制每次循环比对次数.
            if nums[j] > nums[j + 1]:  # 左边数值大于右边.
                nums[j], nums[j + 1] = nums[j + 1], nums[j]  # 交换位置.
                flag = True  # 产生交换,标志置位.
        if not flag:
            return nums
    return nums


def sort_dict():
    sorted()

# 分割线
def dd():
    print('\n', '-' * 20, '这是一条分割线', '-' * 20, '\n', sep='')


# 计算运行时长,把代码块封装成函数,传到计算函数里.
def cal_time(func):
    # 计算函数的运行时间
    start = time.time()
    func()
    end = time.time()
    dp('代码块的运行时长是:%0.2f秒' % (end - start))


def time_diff(strtime, now=datetime.now()):
    # 计算指定时间与当前时间的相差时间。
    if isinstance(strtime, str):  # 传入字符串类型。
        dtime = datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')
    elif isinstance(strtime, list):  # 列表类型
        pass
    else:
        logger.warning(f"请检查传入的时间格式，当前支持：字符串方式和列表形式。")
        return 0


# 错误行
def err_line():
    with open(r"E:\自动化\log\err_line\{}.txt".format(get_date()), 'a', encoding='utf-8') as f:
        f.write(str(traceback.format_exc()) + '\n\n')


# 获取变量名.
def get_var(var):
    frame = sys._getframe(2)
    while frame:
        for item in frame.f_locals.items():
            if (var is item[1]):
                return item[0]
        frame = frame.f_back
    return ''


# 调试变量
def pp(msg, level='DEBUG', color='g', file='D:\checkLog\check_log_debug.txt'):
    if not os.path.exists(file):
        file = './check_log.txt'  # 如果没有，就在当前目录创建日志文件。
    with open(file, 'a') as f:
        f.write(f"{datetime.now()} [{level}] : {msg}\n")
    if color in ['g', 'green', 'GREEN', 'Green']:
        print(f"\033[1;36m{datetime.now()} [{level}] : {msg}\033[0m")
    elif color in ['r', 'red', 'RED', 'Red']:
        print(f"\033[1;31m{datetime.now()} [{level}] : {msg}\033[0m")


# 打印字典信息
def print_dict(dic):
    if isinstance(dic, dict):  # 判断传入的参数是否是字典类型.
        for key, value in dic.items():
            print(f"{key}:{value}")
    else:
        print("传入的数据不是字典类型,请检查输入.")


# 计算函数运行时间的装饰器函数
def runtime(func):
    def inner(*args):
        start = time.time()
        func(*args)
        total = time.time() - start
        print(f"计算时间装饰器:函数运行时间:{total:3.2f}s")
        return 0

    return inner


# 列表去重,且保留顺序.
def set_list(num):  # [1,0,0,0,0,1,1,1,0,0,0,1] ==>[1,0,1,0,1]
    # 这个去重，不是只保留一个，而是把连续重复的，只保留第一个出现的。
    new = []
    for i in num:
        if not new:
            new.append(i)
        else:
            if i != new[-1]:
                new.append(i)
            else:
                pass
    return new


def list_remove(ls1, ls2):
    # 列表1内，去除某些数据。
    for i in ls2:
        try:
            ls1.remove(i)
        except:
            pass


def same_len_str(string, way, width, fill=' ', ):  # 格式输出函数,默认格式填充用单空格,不换行。
    try:
        count = wcwidth.wcswidth(string) - len(string)  # 宽字符数量
        width = width - count if width >= count else 0
        return '{0:{1}{2}{3}}'.format(string, fill, way, width)
    except:
        print('print_format函数参数输入错误！')


@runtime
def ddic():
    i = 0
    while i < 1000000:
        d = {}  # 这样定义字典,效率比dict(),快3倍.
        i += 1


def dict_to_csv(data, file):
    f = open(file, 'a', encoding='utf-8')
    filednames = data.keys()
    info = [data]  # 这里直接传字典.
    csvw = csv.DictWriter(f, filednames, lineterminator='\n')
    csvw.writeheader()
    csvw.writerows(info)  # 这里会处理只要values
    f.close()


def get_devices():
    # 获取所有连接设备的列表
    all_devices = []
    cmd = 'adb devices'
    result = os.popen(cmd).readlines()[1:]
    for item in result:
        if item != "\n":
            all_devices.append(str(item).split("\t")[0])
    # print(get_time(),f"当前连接的设备有：{len(all_devices)}")
    return all_devices  # 设备列表['device113','10.2.8.103:5555',3]


def devices_info():
    cmd = 'adb devices -l'
    devices = []
    result = os.popen(cmd).readlines()[1:-1]  # 抬头和最后的换行符去掉.
    for i in result:
        info = i.split()
        # print(info)
        pad = {}
        pad['serino'] = info[0]
        for j in info:
            # print(j)
            if ':' in j and j != info[0]:
                pad[j.split(':')[0]] = j.split(':')[1]
        # ['PXC6R18308000548', 'device', 'product:HDN-L09', 'model:HDN_L09', 'device:HWHDN-H', 'transport_id:8']
        devices.append(pad)
    print(f"当前电脑,共连接了{len(devices)}个设备.{devices}")


def get_android_version(device):
    if device:
        version = os.popen(f"adb -s {device} shell getprop ro.build.version.release").readline()
        return version
    else:
        version = os.popen(f"adb shell getprop ro.build.version.release").readline()
        return version


def do_something(devices):
    while True:
        os.system(f"adb -s {str(devices)} shell input keyevent 25")
        time.sleep(1)
        os.system(f"adb -s {str(devices)} shell input keyevent 24")


def more_device():
    # 多设备执行自动化。
    devices = get_devices()
    threads = []
    for item in devices:
        # print(item)
        t = threading.Thread(target=do_something, args=(item,))  # 参数记得加逗号，不然item会被变成迭代器，字符串被打散成列表。
        threads.append(t)
    for tt in threads:
        tt.start()


def ainb(a, b):
    # 函数功能,确认短的列表是不是长列表的子列表.
    if len(a) > len(b):  # 默认a是短的
        a, b = b, a
    for i in a:
        if i in b:
            pass
        else:
            return False
    return True


def reset_keyboard(device):
    try:
        tmp_keyboard = os.popen(f"adb -s {device} shell ime list -s").readlines()
        # ['com.baidu.input_huawei/.ImeService\n', 'io.appium.settings/.UnicodeIME\n']
        input_keyboard = [i.replace('\n', '') for i in tmp_keyboard if 'io.appium.settings' not in i]
        os.system(f"adb -s {device} shell ime set {input_keyboard[0]}")
        logger.debug(f"设置设备:{device}的输入法为:{input_keyboard[0]}")
    except:
        logger.debug(f"恢复设备{device}的输入法失败.")


def mychar():
    special = '~!@#$%^&*( )-_/?.,>[]==+'
    alph = string.ascii_letters
    num = '0123456789'
    jap = 'おはようございますこんにちははじめまして、どうぞお愿（ねが）いいたします'
    kor = '생일 축하합니다새해복 많이받세요감사합니다 ! 고맙습니다그래요? 그렇습니까?'
    ch = '的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民'
    ls = special + alph + num + jap + kor + ch
    chr_text = random.sample(ls, random.randint(1, 30))
    return ''.join(chr_text)


def any_one(list_a, list_b):
    if set(list_a) & set(list_b):
        return True
    else:
        return False


def random_string(num=10):
    ls = string.ascii_letters + string.digits + '~!@#$%^&*() '
    return ''.join(random.sample(ls, random.choice(range(1, num))))


def alpha_digit(num=10):
    ls = string.ascii_letters + string.digits
    return ''.join(random.sample(ls, random.choice(range(1, num))))


def random_time():
    x = [str(i).zfill(2) for i in list(time.localtime())][:6]  # 时间戳
    x.append(str(random.choice(range(1000))))
    # random.shuffle(x)  # 原地打乱列表顺序.
    y = int(''.join(x))  # 拼接,转型.
    return y  # 长度为17


def deep_flatten(ls):
    temp = []  # 临时存储

    def f(ls):  # 内嵌函数
        if isinstance(ls, Iterable):  # 判断是否是可迭代对象
            for i in ls:  # 循环抓迭代器里的元素
                for a in f(i):  # 调用自身.
                    temp.append(a)  # 是迭代器里,拆出来,加整到临时列表里.
            return []  # 外层for循环执行完,返回的空列表,不会影响临时列表的值.
        else:
            return [ls]  # 不是迭代器,说明已经无法再展开了.

    f(ls)
    return temp


def binlocation(locate=''):
    shelf = ['01', '02', '03', '04', '05', '06', '07']  # 货架
    row = ['01', '02']  # 排
    floor = ['01', '02']  # 层
    location = ['01', '02', '03', '04']  # 位
    ll = itertools.product(shelf, row, floor, location)
    if not locate:
        return 'A' + ''.join(random.choice(list(ll)))
    return 'A01010101'


def interset(a, b):
    # 两个迭代序列的交集.列表,元组.
    return set(a) & set(b)


def len_same(a, b):
    # 两个序列的交集长度.
    return len(interset(a, b))


def len_diff(a, b):
    # 两个序列差值集合长度，先后顺序有点关系。
    if len(a) >= len(b):
        set1 = set(a)
        set2 = set(b)
    else:
        set1 = set(b)
        set2 = set(a)
    return len(set1 - set2)


def text_in_list(text="", ls=''):
    # 某个文本是否在序列中。
    try:
        if text in ''.join(ls):
            return 1
        return 0
    except:
        logger.warning(f"文本[{text}]是否存在于序列[{ls}]中检查出错，请检查输入的参数。")


def el_index(value, ls):
    # 某个元素在列表里的索引。index就填写+1，-1这样的对应关系。
    return ls.index(value)


def app_screenshot(device='', file_name=''):
    if not get_devices():
        logger.warning("当前电脑没有连接任何一个Android设备,无法进行截屏操作.请检查设备连接情况.")
        return
    if len(get_devices()) > 1 and device == '':
        device = get_devices()[0]
    dir = "D:\AutomationScreen"  # 创建存放截图的电脑文件夹
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = '/sdcard/lxb_shoot'  # 存放截图的平板文件夹
    if not file_name:
        file_name = 'ScreenShoot' + file_time()  # 没有指定文本名称时,使用时间戳
    cmd = f'-s {device}'
    exec_cmd = cmd if len(cmd) > 5 else ''
    try:
        os.system(f"adb {exec_cmd} shell mkdir -p {path}")  # 先创建一个文件夹
    except:
        pass
    os.system(f"adb {exec_cmd} shell screencap -p {path}/{file_name}.png")
    logger.debug(f"截图成功,截图存放位置:{path}/{file_name}.png")
    time.sleep(1)
    os.system(f"adb {exec_cmd} pull {path}/{file_name}.png {dir}")
    logger.debug(f"截图下载到本机成功,截图存放位置:{dir}\\{file_name}.png")  # windows是反斜杠.


def app_screenrecord(device='', file_name='', timeout=30):
    # 录屏 adb shell screenrecord --time-limit 180 /sdcard/screenrecord/demo1.mp4
    # 注意:部分设备,禁用了录屏命令. screenrecord not found
    if not get_devices():
        logger.warning("当前电脑没有连接任何一个Android设备,无法进行截屏操作.请检查设备连接情况.")
        return
    dir = "D:\ScreenRecord"  # 创建存放截图的电脑文件夹
    if not os.path.exists(dir):
        os.makedirs("D:\ScreenRecord")
    path = '/sdcard/screenrecord'  # 存放截图的平板文件夹
    if not file_name:
        file_name = 'ScreenRecord' + file_time()  # 没有指定文本名称时,使用时间戳
    cmd = f'-s {device}'
    exec_cmd = cmd if len(cmd) > 5 else ''
    try:
        os.system(f"adb {exec_cmd} shell mkdir -p {path}")  # 先创建一个文件夹
    except:
        pass
    os.system(f"adb {exec_cmd} shell screenrecord --time-limit {timeout} {path}/{file_name}.mp4")
    logger.debug(f"录屏成功,截图存放位置:{path}/{file_name}.mp4")
    time.sleep(1)
    os.system(f"adb {exec_cmd} pull {path}/{file_name}.mp4 {dir}")
    logger.debug(f"录屏文件下载到本机成功,截图存放位置:{dir}\\{file_name}.mp4")  # windows是反斜杠.


def get_host_ip():
    # 获取本机IP地址.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))  # 这里填网关
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def check_app(device='', appname='com.syriusrobotics.platform.launcher'):
    # 检查安卓设备上指定设备是否在运行。
    info = f'-s {device}' if device else ''
    data = os.popen(f'adb {info} shell ps | findstr {appname}').readline()
    return 1 if data else 0


def read_yaml(file, key=None):
    with open(file, encoding='utf-8') as f:
        value = yaml.load(stream=f, Loader=yaml.FullLoader)
        if key:
            return value[key] if value[key] else f'No value: {key}'
        return value


def write_yaml(file, data=None, mode='a'):
    if file and isinstance(data, dict):
        with open(file, encoding='utf-8', mode=mode) as f:
            yaml.dump(data, stream=f, allow_unicode=True)
    else:
        logger.debug(f"请检查输入文件路径或存入的数据类型是否是键值对。")


def clear_yaml(file):
    with open(file, encoding='utf-8', mode='w') as f:
        f.truncate()  # 清空，好像数据库清空表也是这个命令。


def update_yaml(file, data, mode='w'):
    # 暂时没有好的办法能直接改指定的键值对，全读出来，再写进去，可能是最好的办法。
    value = read_yaml(file)  # 读出来
    # print(data)
    for k, v in data.items():
        value[k] = v
    write_yaml(file, data=value, mode=mode)  # 再写进去。


def get_filename():
    name = str(__file__).split('\\')[-1].split('.')[0]
    return name


class just_err(Exception):

    def __init__(self, message=''):
        if message:
            logger.warning(f"发生自定义异常:{message},请检查一下.")
        else:
            logger.warning("发生了自定义的异常,请检查.")


if __name__ == '__main__':
    print(datetime.now())
