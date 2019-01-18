# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket

from multiplication_client.python.my_test_thrift.gen_py.first_thrift.FirstThriftService import *
from multiplication_client.python.my_test_thrift.gen_py.first_thrift.ttypes import *

"""
   first edit thrift service
   @author xingguo
   @date 1/18/2019 4:28 PM 
   @since 1.0.0 
"""


class FirstThriftHandler:
    """
       thrift 实现类
       @author xingguo
       @date 1/18/2019 4:39 PM
       @since 1.0.0
    """

    def sayHello(self):
        print("调用FirstThriftService:sayHello")


def server_start():
    # 创建服务端
    handler = FirstThriftHandler()
    processor = Processor(handler)
    # 设置服务端指定端口
    # 监听端口
    transport = TSocket.TServerSocket('localhost', 8082)

    # 选择传输层
    tfactory = TTransport.TBufferedTransportFactory()

    # 选择传输协议
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # 创建服务端
    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
    server.setNumThreads(5)

    logging.info('start thrift serve in python')
    server.serve()
    logging.info('done!')


if __name__ == '__main__':
    server_start()
