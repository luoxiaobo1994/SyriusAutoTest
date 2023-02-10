# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/2/9 13:55
# Desc: 自己写的log函数。

import os
from datetime import datetime
from base.common import get_date


class Logger():

    def __init__(self, name='Syrius', file=rf"D:\checkLog\{get_date()}debuglog.txt", level=0, path=''):
        self.level = level
        self.file = file
        self.path = path
        self.name = name

    def debug(self, message, rank='DEBUG', level=0, color='g'):
        self.pp(message, rank=rank, isprint=level, color=color)

    def info(self, message, rank='INFO', level=1, color='p'):
        self.pp(message, rank=rank, isprint=level, color=color)

    def warning(self, message, rank='WARNING', level=2, color='y'):
        self.pp(message, rank=rank, isprint=level, color=color)

    def error(self, message, rank='ERROR', level=3, color='r'):
        self.pp(message, rank=rank, isprint=level, color=color)

    def pp(self, message, rank='DEBUG', color='g', isprint=0):
        data = f"{self.name} {datetime.now()} [{rank}] : {message}\n"
        try:
            with open(self.file, 'a', encoding='utf-8') as f:  # 需要指定utf8编码，不然写一些特殊字符会挂掉。
                f.write(data)
        except Exception as e:
            print(f"\033[1;31m{self.name} {datetime.now()} [{rank}] :"
                  f" 发生异常：{e}。日志写入失败，请检查：[{data}]\033[0m")
        if isprint >= self.level:  # 控制是否在控制台打印。
            if color in ['g', 'green', 'GREEN', 'Green']:  # debug
                print(f"\033[1;36m{self.name} {datetime.now()} [{rank}] : {message}\033[0m")
            elif color in ['p', 'purple', 'PURPLE', 'Purple']:  # info
                print(f"\033[1;35m{self.name} {datetime.now()} [{rank}] : {message}\033[0m")
            elif color in ['y', 'yellow', 'YELLOW', 'Yellow']:  # warning
                print(f"\033[1;33m{self.name} {datetime.now()} [{rank}] : {message}\033[0m")
            elif color in ['r', 'red', 'RED', 'Red']:  # error
                print(f"\033[1;31m{self.name} {datetime.now()} [{rank}] : {message}\033[0m")


if __name__ == '__main__':
    log = Logger(name='luoxiaobo', file=f'tempData/{get_date()}log.txt', level=0)
    log.debug('111')
    log.info('222')
    log.warning('333')
    log.error('444')
