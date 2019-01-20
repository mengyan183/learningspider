import thriftpy2

from thriftpy2.rpc import client_context

from thrift_test.multiplication_client.python.first_thirft_zookeeper.zkconfig.zk_watcher import ZkWatcher

RPCThriftServiceThrift = thriftpy2.load("../thrift/RPCThriftService.thrift", module_name="RPCThriftService_thrift")


class RpcClient():
    def __init__(self, zk_host, app_name):
        self.zk_host = zk_host
        self.app_name = app_name
        self.zk_client = ZkWatcher(hosts=self.zk_host, app_name=self.app_name)

    def request(self):
        host, port = self.zk_client.get_balance_node()
        with client_context(RPCThriftServiceThrift.RPCThriftService, host, port) as c:
            response = c.getHello("xingguo")
            print(response)
            c.sayHello()


if __name__ == '__main__':
    client = RpcClient('127.0.0.1:2181', 'RPCThriftService')
    client.request()
