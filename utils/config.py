# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/4 20:03

import os
from utils.file_reader import YamlReader

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]  # D:\py_projects\Test_framework
CONFIG_FILE = os.path.join(BASE_PATH,'config','config.yml')  # 拼接路径,保证文件路径正确
DATA_PATH = os.path.join(BASE_PATH,'data')
DRIVER_PATH = os.path.join(BASE_PATH,'drivers')
LOG_PATH = os.path.join(BASE_PATH,'log')
REPORT_PATH = os.path.join(BASE_PATH,'report')
# print(COFIG_FILE,DATA_PATH,DRIVER_PATH,LOG_PATH,REPORT_PATH)

class Config():
    def __init__(self,config=CONFIG_FILE):
        self.config = YamlReader(config).data
        # print(type(self.config))   # 可以直接读取到ymal文件了.-->['URL:https://www.baidu.com']

    def get(self,element,index=0):
        return self.config[index].get(element)



if __name__ == '__main__':
    # print(Config().get("URL"))
    print(Config(r'../config/config_gncc.yml').get("Home"))