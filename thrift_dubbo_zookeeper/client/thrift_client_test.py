# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
from thrift_dubbo_zookeeper.zookeeper.zookeeper_first_test import ZookWatcher

"""
   @author xingguo
   @date 1/18/2019 11:39 AM 
   @since 1.0.0 
"""
import thriftpy2

from thriftpy2.rpc import client_context

microservice_thrift = thriftpy2.load("microservice.thrift", module_name="microservice_thrift")


class RpcClient():
    def __init__(self, zookhost, appname):
        self.zookhost = zookhost
        self.appname = appname
        self.zookclient = ZookWatcher(hosts=self.zookhost, appname=self.appname)

    def request(self):
        host, port = self.zookclient.getBalanceNode()
        with client_context(microservice_thrift.MicroService, host, port) as c:
            response = c.doResponse(str(port))
            print(response)


if __name__ == '__main__':
    client = RpcClient('127.0.0.1:2181', 'doResponse')
    client.request()
