# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
"""
    thrift-zookeeper-dubbo
   @author xingguo
   @date 1/18/2019 7:30 AM 
   @since 1.0.0 
"""
from dubbo_zookeeper_thrift import dubbo_zk_manager,dubbo_thrift_manager,base_thrift_client

manager = dubbo_zk_manager
zk_manager = manager.DubboZkManager("127.0.0.1:2181")

