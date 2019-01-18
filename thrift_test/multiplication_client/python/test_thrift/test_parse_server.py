# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket

from multiplication_client.python.test_thrift.parse.Parse import *
from multiplication_client.python.test_thrift.parse.constants import *

"""
   @author xingguo
   @date 1/18/2019 2:40 PM 
   @since 1.0.0 
"""
logging.basicConfig(filename='logger.log', level=logging.INFO,
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class ParseHandler:

    def parseHtml2Xml(self, html):
        logging.info("start parse html")
        print("执行文件解析")


def run():
    # 创建服务端
    handler = ParseHandler()
    processor = Processor(handler)

    # 监听端口
    transport = TSocket.TServerSocket('localhost', 9234)

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
    run()
