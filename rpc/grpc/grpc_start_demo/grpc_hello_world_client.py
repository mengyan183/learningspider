# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
import logging

import grpc

from grpc_start_demo.proto.grpc_python import GrpcHelloWorldService_pb2_grpc
from grpc_start_demo.proto.python import GrpcHelloWorldService_pb2

"""
   grpc hello world service demo
   @author xingguo
   @date 1/25/2019 11:01 AM 
   @since 1.0.0 
"""


def run():
    # 调用 server 服务
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = GrpcHelloWorldService_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(GrpcHelloWorldService_pb2.HelloRequest(name='xingguo'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
