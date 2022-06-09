# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2020/11/30 12:00
import random
import string
import time, csv
import traceback
import sys, os, wcwidth
import threading
from utils.log import Logger
from multiprocessing.dummy import Pool
from collections.abc import Iterable
import itertools

logger = Logger().get_logger()

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
    time_1 = '_'.join(str(i).zfill(2) for i in now_time[3:6])
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


# 分割线
def dd():
    print('\n', '-' * 20, '这是一条分割线', '-' * 20, '\n', sep='')


# 计算运行时长,把代码块封装成函数,传到计算函数里.
def cal_time(func):
    start = time.time()
    func()
    end = time.time()
    dp('代码块的运行时长是:%0.2f秒' % (end - start))


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
def pp(*args):
    for item in args:
        print("变量名为:{}, 变量类型:{}, 变量值:{}".format(get_var(item), type(item), item))


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
    return all_devices


def get_android_version(device):
    version = os.popen(f"adb -s {device} shell getprop ro.build.version.release").readline()
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
    return set(a) & set(b)


class just_err(Exception):

    def __init__(self):
        logger("发生了自定义的异常,出现了某些问题,回查一下.")


if __name__ == '__main__':
    a = [1,2,3]
    b = [2,5,6,3]
    print(interset(a,b))
