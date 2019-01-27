# -*- coding: UTF-8 -*-

import consul


class ConsulConfig:
    def __init__(self, host):
        self.host = host

    def register(self, server_name, ip, port):
        # 连接consul 服务器，默认是127.0.0.1，可用host参数指定host
        c = consul.Consul(host=self.host)
        print(f"开始注册服务{server_name}")
        # 健康检查的ip，端口，检查时间
        check = consul.Check.tcp(ip, port, "10s")
        # 注册服务部分
        c.agent.service.register(server_name, f"{server_name}-{ip}-{port}",
                                 address=ip, port=port, check=check)
        print(f"注册服务{server_name}成功")

    @staticmethod
    def unregister(server_name, ip, port):
        # 取消注册服务
        c = consul.Consul()
        print(f"开始退出服务{server_name}")
        c.agent.service.deregister(f'{server_name}-{ip}-{port}')
