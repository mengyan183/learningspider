# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
import requests
from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket

from multiplication_client.python.test_thrift.parse.Parse import *

"""
   @author xingguo
   @date 1/18/2019 2:50 PM 
   @since 1.0.0 
"""


def run():
    try:
        transport = TSocket.TSocket('localhost', 9234)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = Client(protocol)
        transport.open()

        print('start')
        res = requests.get('https://blog.csdn.net/u011734144/article/details/73848750')
        xml = client.parseHtml2Xml(res.content)
        print(xml)
        transport.close()
    except Thrift.TException as e:
        print('exceptino')
        print(e)


if __name__ == '__main__':
    run()
