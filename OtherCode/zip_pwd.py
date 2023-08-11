# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/8/9 18:34
# Desc:
import threading
import zipfile
from itertools import permutations, combinations, product
import string


def generate_combinations(chars, length):
    # 排列
    perms = product(str(chars), length)
    for perm in perms:
        yield ''.join(perm)
    # 组合
    combs = combinations(chars, length)
    for comb in combs:
        yield ''.join(comb)


def string_generator(characters, length):
    for combination in product(characters, repeat=length):
        yield ''.join(combination)


def extract_zip_file(password_generator):
    zip_path = r"E:\BaiduNetdiskDownload\Python开发实战\Python开发实战.zip"
    while True:
        pwd = next(password_generator)
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(pwd)
            print(f"解压成功！密码是：{pwd}")
            exit(0)  # 成功解压后退出所有线程
        except zipfile.BadZipFile:
            print("文件不是有效的zip文件！")
            break  # 停止尝试提取ZIP文件
        except RuntimeError as e:
            print(f"解压失败,当前密码: {pwd}")
        except Exception as e:
            print(f"发生错误：{str(e)}")


def main():
    for num in range(2,10):
        generator = string_generator(string.ascii_letters + '1234567890', num)  # 替换成你自己的生成器函数
        # 创建多个线程
        num_threads = 40  # 根据需求指定线程数
        threads = []
        for _ in range(num_threads):
            t = threading.Thread(target=extract_zip_file, args=(generator,))
            threads.append(t)
            t.start()

        # 等待所有线程完成
        for t in threads:
            t.join()


if __name__ == '__main__':
    main()
