import unittest

from thrift_test.multiplication_client.python.first_thirft_zookeeper.zkconfig.zkconfig import ZkConfig


class TestThriftZk(unittest.TestCase):
    def test_thrift_server(self):
        pass
        # server = RpcServer('127.0.0.1', 8000, 'doResponse', '127.0.0.1:2181')
        # server.startServer()

    def test_zk_client(self):
        client = ZkConfig(hosts='127.0.0.1:2181')
        client.start_zk()
