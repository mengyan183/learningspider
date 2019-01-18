# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
import unittest

from thrift_dubbo_zookeeper.server.thrift_server_first import RpcServer
from thrift_dubbo_zookeeper.zookeeper.zk_watcher import ZookWatcher
from thrift_dubbo_zookeeper.zookeeper.zookeeper_first_test import ZookeeperClient

"""
   单元测试
   @author xingguo
   @date 1/18/2019 12:58 PM 
   @since 1.0.0 
"""


class TestThriftZk(unittest.TestCase):
    def test_thrift_server(self):
        server = RpcServer('127.0.0.1', 8000, 'doResponse', '127.0.0.1:2181')
        server.startServer()

    def test_zk_client(self):
        client = ZookeeperClient(hosts=self.zookhost)

    def test_zk_watcher(self):
        watcher = ZookWatcher("127.0.0.1", "doResponse")
