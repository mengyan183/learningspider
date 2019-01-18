import re
from difflib import SequenceMatcher

import pypinyin
import zhon
from pypinyin import pinyin
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket, TTransport
from zhon.hanzi import punctuation

from multiplication_client.python.gen_py.similarityservice import ChatSimilarityService

__HOST = '127.0.0.1'
__PORT = 9090


def similar_num(list1, list2):
    return len(set(list1).intersection(list2))


def similar_ration(str1, str2):
    return SequenceMatcher(lambda x: x == ' ', str1, str2).ratio()


class SimilarityHandler(ChatSimilarityService.Iface):
    def __init__(self):
        self.log = {}

    def ping(selfs):
        print('ping')

    def similarity(self, chat1, chat2):
        # 去掉中文字符串中的特殊标点符号
        list1 = re.findall('[^{}]'.format(zhon.hanzi.punctuation), chat1)
        list2 = re.findall('[^{}]'.format(zhon.hanzi.punctuation), chat2)

        # 将标点符号转换成拼音
        pinyin1 = pinyin(list1, style=pypinyin.STYLE_NORMAL)
        pinyin2 = pinyin(list2, style=pypinyin.STYLE_NORMAL)

        # 将所有的拼音统一保存到 单个list 中
        pinyin_list1 = [word[0] for word in pinyin1]
        pinyin_list2 = [word[0] for word in pinyin2]

        # 计算 list 中元素相同的个数
        result1 = similar_num(pinyin_list1, pinyin_list2)

        # list convert to string
        str1_pinyin = ''.join(pinyin_list1)
        str2_pinyin = ''.join(pinyin_list2)
        # 计算字符串的相似度
        result2 = similar_ration(str1_pinyin, str2_pinyin)

        print('ratio:{}, nums:{}'.format(result2, result1))
        return result2


if __name__ == '__main__':
    handler = SimilarityHandler()
    processor = ChatSimilarityService.Processor(handler)
    transport = TSocket.TServerSocket(host=__HOST, port=__PORT)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

    print('Starting the server')
    server.serve()
    print('done')
