# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/3 16:20


import openpyxl
import os

class ExcelUtil():

    def get_object_path(self):
        # 获取项目路径,保证excel的路径是正确的.
        print(os.path.dirname(__file__))

    def read_excel(self):
        openpyxl.load_workbook()


if __name__ == '__main__':
    ExcelUtil().get_object_path()