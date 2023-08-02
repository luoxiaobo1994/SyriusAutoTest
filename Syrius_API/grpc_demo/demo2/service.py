# -*- coding:utf-8 -*-
# Author: luoxiaobo
# 2023/4/21 9:38
# Describe: demo实例的服务端

import grpc  # 必要导入
import Demo_pb2 as pb2
import Demo_pb2_grpc as pb2_grpc
from concurrent import futures  #  线程数量支持


class DemoTest(pb2_grpc.DemoTestServicer):

    def DemoReq(self, request, context):
        name = request.name
        age = request.age
        result = f"My name is {name}, I'm {age} years old!"
        return pb2.OneResponse(result=result)  # 这里读不到报警，可能是插件问题，查询一下。


def run():
    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4)  # 最大的工作线程数量
    )
    pb2_grpc.add_DemoTestServicer_to_server(DemoTest(), grpc_server)
    host = '127.0.0.1:5000'
    grpc_server.add_insecure_port(f"{host}")
    grpc_server.start()
    print(f"grpc server start at host: {host}...")
    grpc_server.wait_for_termination()

if __name__ == '__main__':
    run()

