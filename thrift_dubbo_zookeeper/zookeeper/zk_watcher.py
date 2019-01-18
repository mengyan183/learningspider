# -*- coding: UTF-8 -*-
from random import randint

from kazoo.client import KazooClient

from thrift_dubbo_zookeeper.server.thrift_server_first import RpcServer


class ZookWatcher():
    def __init__(self, hosts, appname):
        self.kazooclient = KazooClient(hosts=hosts)
        self.kazooclient.start()
        self.appname = appname
        self.nodelist = self.getChildren()
        self.watchNode()

    def getChildren(self):
        if self.kazooclient.exists('/' + self.appname):
            return self.kazooclient.get_children('/' + self.appname)
        return None

    def watchNode(self):
        self.kazooclient.get_children(self.appname, self.watchFunc())

    # 监控服务
    def watchFunc(self):
        nodeList = self.getChildren()
        # 如果节点不存在
        for node in self.nodelist:
            if node not in nodeList:
                server = RpcServer(host=self.host, port=node, appname=self.appname)
                server.startServer()
                print('over')

    def getBalanceNode(self):
        node = self.nodelist[randint(0, len(self.nodelist) - 1)]
        host = node.split(':')[0]
        port = int(node.split(':')[1])
        return host, port
