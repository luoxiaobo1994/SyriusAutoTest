# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/4 20:05

import os

import yaml
from xlrd import open_workbook


class YamlReader():

    def __init__(self, yamlf):

        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileExistsError("文件不存在!")
        self._data = None  # 私有属性

    @property
    def data(self):
        # 如果是第一次调用data,读取yaml文档,否则返回之前保存的数据
        if not self._data:  # 如果不存在,则读取.
            with open(self.yamlf, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))  # load返回的是一个生成器,需要list转换
        return self._data[0]


class SheetTypeError(Exception):
    pass


class ExcelReader():
    """
    读取Excel文件中的内容,返回list.
    如:
    excel的内容为:
    |A|B       |C     |
    |1|zhangsan|123456|
    |2|admin   |lxb123|

    如果 print(ExcelReader(excel,title_line=True).data),输出结果:
    [{"A":1,"B":zhangsan,"C":123456},{"A":2,"B":admin,"C":lxb123}]
    如果 print(ExcelReader(excel,title_line=False).data),输出结果:
    [["A","B","C"],[1,zhangsan,123456],[2,admin,lxb123]]

    可以指定sheet,通过index或者name
    ExcelReader(excel,sheet=2)
    ExcelReader(excel,sheet="账号密码表")
    """

    def __init__(self, excel, sheet=0, title_line=True):
        if os.path.exists(excel):
            self.excel = excel
        else:
            raise FileNotFoundError("文件不存在,请检查路径!")
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()

    @property
    def data(self):
        if not self._data:
            workbook = open_workbook(self.excel)
            if type(self.sheet) not in [int, str]:
                raise SheetTypeError("请输入正确的表单序号或名称,而不是输入{0}".format(type(self.sheet)))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            else:
                s = workbook.sheet_by_name(self.sheet)

            if self.title_line:
                title = s.row_values(0)
                for col in range(1, s.nrows):
                    # 依次遍历其余行.与首行组成字典,拼接到self._data中
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                for col in range(0, s.nrows):
                    # 遍历所有行,拼到self._data中
                    self._data.append(s.row_values(col))
        return self._data


if __name__ == '__main__':
    y = '../config/speedpicker_config.yaml'
    reader = YamlReader(y)
    print(reader.data['sp_text'])
