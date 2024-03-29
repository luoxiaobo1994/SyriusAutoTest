# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/2/9 13:55
# Desc: 自己写的log函数。

import os
from datetime import datetime
from base.common import get_date


class Logger():

    def __init__(self, file, name='Syrius', isprint=0, path='./'):
        self.isprint = isprint  # 控制台输出等级
        self.file = file  # 日志存储地址
        self.path = path  # scp文件的传输目标地址
        self.name = name  # 日志名称

    def debug(self, message, level='DEBUG', isprint=0, color='g'):
        self.pp(message, level=level, isprint=isprint, color=color)

    def info(self, message, level='INFO', isprint=1, color='p'):
        self.pp(message, level=level, isprint=isprint, color=color)

    def warning(self, message, level='WARNING', isprint=2, color='y'):
        self.pp(message, level=level, isprint=isprint, color=color)

    def error(self, message, level='ERROR', isprint=3, color='r'):
        self.pp(message, level=level, isprint=isprint, color=color)

    def pp(self, message, level='DEBUG', color='g', isprint=0):
        data = f"{self.name} {datetime.now()} [{level}] : {message}\n"
        try:
            with open(file=self.file, mode='a', encoding='utf-8', buffering=4096) as f:  # 需要指定utf8编码，不然写一些特殊字符会挂掉。
                f.write(data)
                f.flush()
        except Exception as e:
            print(f"\033[1;31m{self.name} {datetime.now()} [{level}] :"
                  f" 发生异常：{e}。日志写入失败，请检查：[{data}]\033[0m")
        if isprint >= self.isprint:  # 控制是否在控制台打印。
            log_data = f"{self.name} {datetime.now()} [{level}] : {message}"
            if color in ['g', 'green', 'GREEN', 'Green']:  # debug
                # print(f"\033[1;32m{log_data}\033[0m")  # 青绿色
                print(f"{log_data}")  # 白色
            elif color in ['p', 'purple', 'PURPLE', 'Purple']:  # info
                print(f"\033[1;36m{log_data}\033[0m")
            elif color in ['y', 'yellow', 'YELLOW', 'Yellow']:  # warning
                print(f"\033[1;93m{log_data}\033[0m")
            elif color in ['r', 'red', 'RED', 'Red']:  # error
                print(f"\033[1;31m{log_data}\033[0m")


if __name__ == '__main__':
    log = Logger(name='luoxiaobo', file=f'tempData/{get_date()}log.txt', isprint=0)
    log.debug('启动脚本...')
    log.info('222')
    log.warning('333')
    log.error('444')
