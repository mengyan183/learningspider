# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
# 引入urllib
import json
import time
from urllib import request, parse

# 引入requests
# 引入chardet
import chardet

"""
    urllib测试
   @author xingguo
   @date 1/7/2019 4:11 PM 
   @since 1.0.0 
"""


def urllib_first_test(url, headers):
    """
       @author guoxing
       @date 1/7/2019 4:13 PM
       @since 1.0.0
       Returns:

       使用urllib.request发送请求
    """
    # 创建request请求
    new_request = request.Request(url=url, headers=headers)
    # 获取响应
    new_response = request.urlopen(new_request)
    print("geturl打印信息：%s" % (new_response.geturl()))
    print('**********************************************')
    print("info打印信息：%s" % (new_response.info()))
    print('**********************************************')
    print("getcode打印信息：%s" % (new_response.getcode()))
    # 获取返回结果
    read = new_response.read()
    # 获取网页编码格式,使用chardet库
    detect = chardet.detect(read)
    encode = detect.get("encoding")
    # 解析
    decode_html = read.decode(encode)
    # 打印获取的网页数据
    print(decode_html)


def urllib_youdao_translate_test(text):
    """
        有道英文转换为中文翻译测试
       @author xingguo
       @date 1/7/2019 5:29 PM
       @since 1.0.0
       TODO:当前请求有道翻译存在bug
    """
    # 定义headers
    headers = {}
    headers['Cookie'] = "_ntes_nnid=57bfa53adb528cbe2374cf8ecabf98f6,1530094669030; OUTFOX_SEARCH_USER_ID_NCOO=557542320.3846598; OUTFOX_SEARCH_USER_ID=125550975@10.169.0.83; JSESSIONID=aaaTd_I7UhdeedVO9ONGw; ___rl__test__cookies=1546853294698"
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    headers['Referer'] = "http://fanyi.youdao.com/"
    # 有道翻译(英文转换为中文)
    youdao_translate_url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    # 参数
    form_data = {"i": "test",
                 "from": "AUTO",
                 "to": "AUTO",
                 "smartresult": "dict",
                 "client": "fanyideskweb",
                 "salt": 15468532947005,
                 "sign": "c3866c1e9c0632421a1a7b390e875c22",
                 "bv": "363eb5a1de8cfbadd0cd78bd6bd43bee",
                 "doctype": "json",
                 "version": 2.1,
                 "keyfrom": "fanyi.web",
                 "action": "FY_BY_CLICKBUTTION",
                 "typoResult": "false"}
    auto_data = {"ts": time.time()}
    # 字典类型追加
    form_data.update(auto_data)
    form_data["i"] = text
    # 使用urlencode方法转换标准格式
    data = parse.urlencode(form_data).encode('utf-8')
    # 包装request对象
    request_request = request.Request(url=youdao_translate_url, headers=headers,data=data)
    # 传递Request对象
    response = request.urlopen(request_request)
    read = response.read()
    detect = chardet.detect(read)
    # 读取信息并解码
    html = read.decode(detect["encoding"])
    # 使用JSON
    translate_results = json.loads(html)
    # 如果正常返回
    if translate_results["errorCode"] == 0:
        # 找到翻译结果
        translate_results = translate_results['translateResult'][0][0]['tgt']
        # 打印翻译信息
        print("翻译的结果是：%s" % translate_results)


if __name__ == '__main__':
    url = "https://fanyi.baidu.com"
    # urllib_first_test(url, {})
    urllib_youdao_translate_test("translate")
