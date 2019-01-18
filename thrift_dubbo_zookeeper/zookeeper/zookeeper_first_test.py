# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""


"""
   zkclient 配置
   @author xingguo
   @date 1/18/2019 11:26 AM 
   @since 1.0.0 
"""

import logging

from kazoo.client import KazooClient

logging.basicConfig()


class ZookeeperClient():
    def __init__(self, hosts):
        self.kazooclient = KazooClient(hosts=hosts)
        self.kazooclient.start()

    def foundApp(self, appname):
        if self.kazooclient.exists('/' + appname):
            pass
        else:
            self.kazooclient.ensure_path('/' + appname)

    def foundNode(self, appname, port, host):
        if self.kazooclient.exists('/' + appname + '/' + host + ':' + str(port)):
            pass
        else:
            self.kazooclient.create('/' + appname + '/' + host + ':' + str(port))

    def close(self):
        self.kazooclient.close()

    def register(self, appname, port, host):
        self.foundApp(appname)
        self.foundNode(appname, port, host)
        #self.close()
