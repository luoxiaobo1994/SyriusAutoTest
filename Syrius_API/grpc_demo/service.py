# coding:utf-8

import grpc
import hello_bilibili_pb2 as pb2
import hello_bilibili_pb2_grpc as pb2_grpc
from concurrent import futures

class Bilili(pb2_grpc.BibiliServicer):
    def HelloDewei(self, request, context):
        name = request.name
        age = request.age

        result = f"My name is {name}, I'm {age} years old."
        return pb2.HelloDeweiReply(result=result)

def run():
    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4)
    )
    pb2_grpc.add_BibiliServicer_to_server(Bilili(),grpc_server)
    host = '127.0.0.1:5000'
    grpc_server.add_insecure_port(f'{host}')
    grpc_server.start()
    grpc_server.wait_for_termination()


if __name__ == '__main__':
    run()