# coding: utf-8

import grpc
import hello_bilibili_pb2 as pb2
import hello_bilibili_pb2_grpc as pb2_grpc


def run():
    host = '127.0.0.1:5000'
    conn = grpc.insecure_channel(host)
    client = pb2_grpc.BibiliStub(channel=conn)
    response = client.HelloDewei(pb2.HelloDeweiReq(
        name='dewei',
        age=33
    ))
    print(response.result)

if __name__ == '__main__':
    run()
