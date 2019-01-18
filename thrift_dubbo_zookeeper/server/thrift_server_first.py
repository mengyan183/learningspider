# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
import thriftpy2
from thriftpy2.rpc import make_server

from thrift_dubbo_zookeeper.zookeeper.zookeeper_first_test import ZookeeperClient

"""
   创建thrift-server端
   @author xingguo
   @date 1/18/2019 11:22 AM 
   @since 1.0.0 
"""

microservice_thrift = thriftpy2.load("../thrift_code/microservice.thrift", module_name="microservice_thrift")


class Dispatcher(object):
    def doResponse(self, a):
        print("doReponse!")
        return 'response is' + a


class RpcServer():
    def __init__(self, host, port, appname, zookhost):
        self.port = port
        self.host = host
        self.appname = appname
        self.zookhost = zookhost

    def startServer(self):
        server = make_server(microservice_thrift.MicroService, Dispatcher(),
                             self.host, self.port)
        client = ZookeeperClient(hosts=self.zookhost)
        client.register(self.appname, self.port, self.host)
        server.serve()  # 启动服务


if __name__ == '__main__':
    server = RpcServer('127.0.0.1', 8000, 'doResponse', '127.0.0.1:2181')
    server.startServer()
