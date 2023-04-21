# -*- coding:utf-8 -*-
# Author: luoxiaobo
# 2023/4/21 9:50
# Describe: demo实例的客户端


import grpc
import Demo_pb2 as pb2
import Demo_pb2_grpc as pb2_grpc

"""
客户端实例，不需要再创建一个类，直接是run函数跑起来。
host和服务端的对应，这里最好搞配置文件，读取一致的。
"""


def run():
    host = '127.0.0.1:5000'
    conn = grpc.insecure_channel(host)
    client = pb2_grpc.DemoTestStub(channel=conn)
    response = client.DemoReq(
        pb2.OneRequest(
            name='luoxiaobo',
            age=99
        )
    )
    print(response.result)


if __name__ == '__main__':
    run()
