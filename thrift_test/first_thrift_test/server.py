# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport

from first_thrift_test.example import Example

"""
   @author xingguo
   @date 1/18/2019 1:11 PM 
   @since 1.0.0 
"""


def start_server():
    try:
        transport = TSocket.TSocket(host='192.168.89.112', port=8081)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Example.Client(protocol)
        transport.open()
        print(client.ping())
        client.say('Hello from Python!')
        transport.close()

    except Thrift.TException as tx:
        print(tx.message)


if __name__ == '__main__':
    start_server()
