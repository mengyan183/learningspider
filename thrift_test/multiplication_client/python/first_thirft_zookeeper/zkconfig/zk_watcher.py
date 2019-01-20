# -*- coding: UTF-8 -*-
from random import randint

from kazoo.client import KazooClient

from thrift_test.multiplication_client.python.first_thirft_zookeeper.service.first_thirft_zk_server import RpcServer


class ZkWatcher:
    def __init__(self, hosts, app_name):
        self.hosts = hosts
        self.kazoo_client = KazooClient(hosts=hosts)
        self.kazoo_client.start()
        self.app_name = app_name
        self.nodelist = self.get_children()
        self.watch_node()

    def get_children(self):
        # 获取所有子节点
        if self.kazoo_client.exists('/' + self.app_name):
            return self.kazoo_client.get_children('/' + self.app_name)
        return None

    def watch_node(self):
        # 查找节点
        self.kazoo_client.get_children(self.app_name, self.watch_func())

    # 监控服务
    def watch_func(self):
        # 获取所有子节点
        node_list = self.get_children()
        # 如果节点不存在
        for node in self.nodelist:
            if node not in node_list:
                server = RpcServer(host=self.hosts, port=node, app_name=self.app_name)
                server.start_server()
                print('over')

    def get_balance_node(self):
        node = self.nodelist[randint(0, len(self.nodelist) - 1)]
        host = node.split(':')[0]
        port = int(node.split(':')[1])
        return host, port
