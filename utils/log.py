# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/4 19:45

import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler


class Logger(object):

    def __init__(self, log_name="Syrius", file='log.txt'):
        self.logger = logging.getLogger(log_name)
        logging.root.setLevel(logging.NOTSET)  # 日志级别,NOTEST是比DEBUG还低一级的级别,就是全部输出了.
        self.logger_file_name = self.file_day() + file  # 生成的文件名称.2022-6-20_log.txt
        self.backup_count = 30  # 备份的最大数量,多保存几份.
        # 日志输出级别
        self.console_output_level = "DEBUG"  # 控制台输出所有信息,实际调试的时候,脚本有控制,这里不一定生效.
        self.file_output_level = "DEBUG"  # 日志文件仅输出信息.尽量保存得详细些
        # 日志输出格式,可以修改一下日期格式,避免出现三位数的毫秒.
        self.formatter = logging.Formatter("%(name)s %(asctime)s [%(levelname)s] : %(message)s",
                                           datefmt='%Y-%m-%d %H:%M:%S')
        self.create_logdir()  # 判断是否有文件夹,没有就先创建一个.

    def create_logdir(self):
        dir = "D:\AutomationLog"
        if not os.path.exists(dir):
            os.makedirs("D:\AutomationLog")

    def file_day(self):
        # 按天生成文件.
        now_time = time.localtime()  # [2020, 11, 30, 12, 3, 5, 0, 335, 0]
        date_1 = '-'.join(str(i).zfill(2) for i in now_time[:3])
        return date_1 + '_'

    def get_logger(self):
        """在logger中添加日志句柄并返回,如果logger已有句柄,则直接返回"""
        if not self.logger.handlers:  # 避免重复日志
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # 每天重新创建一个日志文件,最多保存backup_count份,避免硬盘消耗.
            file_handler = TimedRotatingFileHandler(
                filename=os.path.join("D:\AutomationLog", self.logger_file_name),  # 文件名称
                when='D',  # 刷新或生成时间,按秒,分,时,日...生成.
                interval=1,  # 日志文件的刷新间隔,配合when使用的.
                backupCount=self.backup_count,  # 最大备份数量
                delay=True,  # 就是延迟了,源码是False
                encoding="utf-8"  # 编码格式
            )
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger


logger = Logger().get_logger()  # 直接生成日志器, 给其他文件再次调用即可.

if __name__ == '__main__':
    logger.debug("简单调试一下.")
