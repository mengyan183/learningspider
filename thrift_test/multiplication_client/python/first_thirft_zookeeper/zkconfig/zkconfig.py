import sys

from kazoo.client import KazooClient, KazooState
import logging

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                    format='%(asctime)s %(pathname)s %(funcName)s%(lineno)d %(levelname)s: %(message)s')

# 创建一个客户端，可以指定多台zookeeper，
# zk = KazooClient(
#     # 指定多台zk使用"，"分割
#     hosts='127.0.0.1:2181'
#     , timeout=10.0  # 连接超时时间
#     , logger=logging  # 传一个日志对象进行，方便 输出debug日志
# )
# 开始心跳
# zk.start()

# 获取根节点数据和状态
# data, stat = zk.get('/')

'''
这个是stat的输出：
ZnodeStat(czxid=0, mzxid=0, ctime=0, mtime=0, version=0, cversion=8448, aversion=0, ephemeralOwner=0, dataLength=0, numChildren=4, pzxid=4295036257L)
ZnodeState的属性列表:
czxid ： 创建这个节点时的zxid
mzxid : 修改这个节点时的zxid
ctime ： 创建时间
mtime : 修改时间
version : 数据被修改的次数
cversion: 子节点被修改的次数
aversion: acl被改变的次数
ephemeralOwner:临时节点创建的用户，如果不是临时节点值为0
dataLength:节点数据长度
numChildren:子节点的数量
pzxid:子节点被修改的zxid
'''


# 获取根节点的所有子节点，返回的是一个列表，只有子节点的名称
# children = zk.get_children("/")


# 下面是根节点的返回值
# [u'rmstore', u'kazoo', u'yarn-leader-election', u'zookeeper']

# 递归遍历所有节点的子节点函数,_zk是KazooClient的对象，node是节点名称字符串，func是回调函数
# def zk_walk(_zk, node, func):
#     data, stat = _zk.get(node)
#     children = _zk.get_children(node)
#     func(node, data, stat, children);
#     if len(children) > 0:
#         for sub in children:
#             sub_node = ''
#             if node != '/':
#                 sub_node = node + '/' + sub
#             else:
#                 sub_node = '/' + sub
#             zk_walk(_zk, sub_node, func)


# 测试zk_walk的打印回调函数，只是把所有数据都打印出来
# def printZNode(node, data, stat, children):
#     print("node  : " + node)
#     print("data  : " + str(data))
#     print("stat  : " + str(stat))
#     print("child : " + str(children))
#     print('\n')


# 遍历谋个节点的所有子节点
# zk_walk(zk, '/', printZNode)


class ZkConfig:
    def __init__(self, hosts):
        # 构造zkclient
        self.kazoo_client = KazooClient(
            # 指定多台zk使用"，"分割
            hosts=hosts,
            # 连接超时时间
            timeout=10.0,
            # 传一个日志对象进行，方便 输出debug日志
            logger=logging
        )

    def start_zk(self):
        # zk启动心跳
        self.kazoo_client.start()

    def found_app(self, app_name):
        # 查找服务
        if self.kazoo_client.exists('/' + app_name):
            pass
        else:
            self.kazoo_client.ensure_path('/' + app_name)

    def found_node(self, app_name, port, host):
        # 查找节点
        if self.kazoo_client.exists('/' + app_name + '/' + host + ':' + str(port)):
            pass
        else:
            self.kazoo_client.create('/' + app_name + '/' + host + ':' + str(port))

    def register(self, app_name, port, host):
        # 注册服务
        self.found_app(app_name)
        self.found_node(app_name, port, host)

    def zk_close(self):
        # zk关闭
        zk = self.kazoo_client
        # 执行stop后所有的临时节点都将失效
        zk.stop()
        zk.close()