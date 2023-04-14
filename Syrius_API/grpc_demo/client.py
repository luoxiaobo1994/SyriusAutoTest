# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/4/13 17:42
# Desc: grpc 客户端文件

import grpc
import demo_pb2 as pb2
import demo_pb2_grpc as pb2_grpc

def run():
    conn = grpc.insecure_channel('127.0.0.1:5000')  # 连接前面绑定的客户端。
    client = pb2_grpc.DemoStub(channel=conn)
    respone = client.Demo(pb2.DemoReq(
        name = '罗小波'
        age = 30
    ))
    print(respone)
