# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/7/23 14:18
# Desc: 信号量，多线程对文件进行读写时的限制。
import threading
from threading import Semaphore
from time import sleep

sem = Semaphore(value=4)  # 锁数量


class Html(threading.Thread):
    # 模拟获取网页数据

    def __init__(self, url, sem):
        super().__init__()
        self.url = url
        self.sem = sem

    def run(self):
        # 模拟IO操作
        sleep(2)
        print(f"获取网页：{self.url}结果成功。")
        self.sem.release()  # 爬取完成，释放锁资源。


class UrlProduce(threading.Thread):

    def __init__(self, sem):
        super().__init__()
        self.sem = sem

    def run(self):
        for i in range(20):
            self.sem.acquire()  # 先获取锁
            html_thread = Html(url=f"https://www.baidu.com/{i}/index", sem=self.sem)
            html_thread.start()


if __name__ == '__main__':
    urlproduce = UrlProduce(sem)
    urlproduce.start()
