# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
import logging
import time
from concurrent import futures

import grpc

from grpc_start_demo.consul_config import ConsulConfig
from grpc_start_demo.proto.grpc_python import GrpcHelloWorldService_pb2_grpc
from grpc_start_demo.proto.python import GrpcHelloWorldService_pb2

"""
   grpc hello world service demo
   @author xingguo
   @date 1/25/2019 11:01 AM 
   @since 1.0.0 
"""

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(GrpcHelloWorldService_pb2_grpc.GreeterServicer):
    """
       GrpcHelloWorldService实现类
       @author xingguo
       @date 1/26/2019 2:00 PM
       @since 1.0.0
    """
    def SayHello(self, request, context):
        """
           重写GRPC 发布的 接口服务
           @author xingguo
           @date 1/26/2019 11:19 AM
           @since 1.0.0
        """
        return GrpcHelloWorldService_pb2.HelloReply(message='Hello World, %s!' % request.name)

    def SayHelloAgain(self, request, context):
        return GrpcHelloWorldService_pb2.HelloReply(message="HelloWorldAgain,%s" % request.name)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    GrpcHelloWorldService_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('127.0.0.1:50051')
    # 初始化consul配置
    consul_config = ConsulConfig("127.0.0.1")
    # 注册server
    consul_config.register("hello_grpc_server", "127.0.0.1", 50051)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        consul_config.unregister("hello_grpc_server", "127.0.0.1", 50051)
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
