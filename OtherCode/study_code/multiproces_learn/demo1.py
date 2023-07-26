# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/2 0:07
# Desc: 多进程实例1  1


from multiprocessing import Process
import os

def foo(name):
    print(f"name:{name}")
    print(f"parent process id:{os.getpid()}")
    print(f"sub process id:{os.getpid()}")

if __name__ == '__main__':
    print(f"parent process id2:{os.getpid()}")
    p = Process(target=foo,args=('bob',))  # 开一个子进程
    p.start()
    p.join()  # 阻塞进程，需要等这个进程执行完了。才会进入下一步