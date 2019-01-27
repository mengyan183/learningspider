# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
import logging

import grpc
from dns import resolver
from dns.exception import DNSException

from grpc_start_demo.proto.grpc_python import GrpcHelloWorldService_pb2_grpc
from grpc_start_demo.proto.python import GrpcHelloWorldService_pb2

"""
   grpc hello world service demo
   @author xingguo
   @date 1/25/2019 11:01 AM 
   @since 1.0.0 
"""
# 连接consul服务，作为dns服务器
consul_resolver = resolver.Resolver()
# consul 端口
consul_resolver.port = 8600
# consul 服务地址
consul_resolver.nameservers = ["127.0.0.1"]


def get_ip_port(server_name):
    # 查询出可用的一个ip，和端口
    try:
        dnsanswer = consul_resolver.query(f'{server_name}.service.consul', "A")
        dnsanswer_srv = consul_resolver.query(f"{server_name}.service.consul", "SRV")
    except DNSException:
        return None, None
    return dnsanswer[0].address, dnsanswer_srv[0].port

# 获取其中一个注册服务地址
ip, port = get_ip_port("hello_grpc_server")
print(ip, port)
def run():
    # 调用 server 服务
    with grpc.insecure_channel(f"{ip}:{port}") as channel:
        stub = GrpcHelloWorldService_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(GrpcHelloWorldService_pb2.HelloRequest(name='xingguo'))
        again = stub.SayHelloAgain(GrpcHelloWorldService_pb2.HelloRequest(name="xingguo"))
    print("Greeter client received: " + response.message)
    print("Greeter client received: " + again.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
