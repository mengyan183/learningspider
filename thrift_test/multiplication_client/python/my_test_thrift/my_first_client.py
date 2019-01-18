# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

from multiplication_client.python.my_test_thrift.gen_py.first_thrift.FirstThriftService import Client

"""
    first thrift client
   @author xingguo
   @date 1/18/2019 4:50 PM 
   @since 1.0.0 
"""


def start_client():
    try:
        transport = TSocket.TSocket('localhost', 8082)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Client(protocol)
        transport.open()
        print('start')
        client.sayHello()
        transport.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    start_client()
