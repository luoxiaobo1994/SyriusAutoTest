# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021-07-08 14:33

import os

""" 用于批量更新可更新的第三方库 """


def pip_update():
    print("查询可升级第三方库中,请等待...")
    model_ls = os.popen('pip list -o').readlines()  # 这样才能拿到命令行的返回值.
    # 第一行是名称,第二行是分割线
    up_list = [i.split()[0] for i in model_ls[2:-1]]  # 库信息的排布:'numpy  旧版本 新版本 xx' 按空格分割拿到包名就好
    print(f"可升级的库有:{up_list}")
    for item in up_list:
        if not item.startswith("\\x") and item != 'pip':  # 抓到一个异常数据： '\x1b[0m' . 自动更新pip容易出问题.
            try:
                print('-' * 50, f'开始升级库:{item}', sep='\n')
                os.system(f"pip install --upgrade {item}")
            except:
                print(f"升级错误:{item}")


if __name__ == '__main__':
    pip_update()
