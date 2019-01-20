import thriftpy2
from thriftpy2.rpc import make_server

from thrift_test.multiplication_client.python.first_thirft_zookeeper.zkconfig.zkconfig import ZkConfig

RPCThriftServiceThrift = thriftpy2.load("../thrift/RPCThriftService.thrift", module_name="RPCThriftService_thrift")


class RPCThriftServiceHandler:
    # RPCThriftService 实现类

    def getHello(self, name):
        return "Hello," + str(name)

    def sayHello(self):
        hello = self.getHello("xingguo")
        print(str(hello))


class RpcServer:
    # 构建RPC服务
    def __init__(self, host, port, app_name, zk_host):
        """
            @Description: 构建rpc初始化服务
            @Param:
            :parameter host 当前服务请求地址
            :parameter port 服务端口
            :parameter app_name 暴露服务名称
            :parameter zk_host zk地址
            @Author: xingguo
            @Date: 2019-01-20 
        """
        self.port = port
        self.host = host
        self.app_name = app_name
        self.zk_host = zk_host

    def start_server(self):
        server = make_server(RPCThriftServiceThrift.RPCThriftService, RPCThriftServiceHandler(), self.host, self.port)
        # 构建zk客户端
        client = ZkConfig(hosts=self.zk_host)
        # 开启zk服务
        client.start_zk()
        # 注册服务
        client.register(self.app_name, self.port, self.host)
        # 启动服务
        server.serve()


if __name__ == '__main__':
    # 通过自定义RpcServer 注册 RPCThriftService
    rpc_server = RpcServer('127.0.0.1', 8081, 'RPCThriftService', '127.0.0.1:2181')
    rpc_server.start_server()
