# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
import hashlib
from http import cookiejar
from urllib import request, parse

import chardet
import requests
from bs4 import BeautifulSoup

from dynamic_html_spider.cas_login_param import CasLoginParam

"""
    模拟登录
   @author xingguo
   @date 1/11/2019 8:13 PM 
   @since 1.0.0 
"""


def get_cookie(url):
    """
        获取指定网站COOKIE 数据
       @author xingguo
       @date 1/11/2019 8:16 PM
       @since 1.0.0
    """
    # 创建cookiejar变量存储cookie数据
    cookie_list = cookiejar.CookieJar()
    # 使用request生成cookie handler(解析器)
    processor = request.HTTPCookieProcessor(cookie_list)
    # 使用解析器创建opener
    opener = request.build_opener(processor)
    # 打开网站
    response = opener.open(url)
    # 打印网站cookie信息
    # for cookie in cookie_list:
    #     print('Name = %s' % cookie.name)
    #     print('Value = %s' % cookie.value)
    return cookie_list


def store_cookie_local(url):
    """
        将cookie存储到本地
       @author xingguo
       @date 1/11/2019 8:45 PM
       @since 1.0.0
    """
    # 设置保存cookie的文件，同级目录下的cookie.txt
    filename = 'cookie.txt'
    # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookiejar.MozillaCookieJar(filename)
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此处的open方法打开网页
    response = opener.open(url)
    # 保存cookie到文件
    cookie.save(ignore_discard=True, ignore_expires=True)


def load_cookie_text(cookie_text_path, url):
    """
        从本地cookie文件读取url
       @author xingguo
       @date 1/11/2019 8:52 PM
       @since 1.0.0
    """
    # 设置保存cookie的文件的文件名,相对路径,也就是同级目录下
    filename = cookie_text_path
    # 创建MozillaCookieJar实例对象
    cookie = cookiejar.MozillaCookieJar()
    # 从文件中读取cookie内容到变量
    cookie.load(filename, ignore_discard=True, ignore_expires=True)
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)
    # 此用opener的open方法打开网页
    response = opener.open(url)
    # 打印信息
    # print(response.read().decode("utf8", "ignore"))


url = "http://sso.test.tthunbohui.com/login"
# get_cookie(url)
# store_cookie_local(url)
# load_cookie_text("cookie.txt", url)

headers = {
    "Cache-Control": 'max-age=0',
    "Content-Type": 'application/x-www-form-urlencoded',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/70.0.3538.77 Safari/537.36',
}


def list_cas_arg(login_url):
    """
        获取lt/execution/_eventId参数
       @author xingguo
       @date 1/11/2019 9:30 PM
       @since 1.0.0
    """
    response = requests.get(login_url)
    # 解析响应
    read = response.read()
    detect = chardet.detect(read)
    # 读取信息并解码
    html = read.decode(detect["encoding"], "ignore")
    # 获取jsessionId
    cookies = response.cookies
    cookies_jsessionid_value = cookies["JSESSIONID"]
    print(str(cookies_jsessionid_value))
    # 解析html
    soup = BeautifulSoup(html, "html.parser")
    lt_tag = soup.find("input", {"name": "lt"})
    execution_tag = soup.find("input", {"name": 'execution'})
    event_id_tag = soup.find("input", {"name": '_eventId'})
    submit_tag = soup.find("button", {"name": 'submit'})
    if lt_tag is not None and execution_tag is not None and event_id_tag is not None and submit_tag is not None:
        execution = execution_tag.get("value")
        event_id = event_id_tag.get("value")
        lt = lt_tag.get("value")
        submit = submit_tag.get("value")
        # print(str(lt))
        # print(str(execution))
        # print(str(event_id))
        # print(str(submit))
        cas_login_param = CasLoginParam(None, None, None, None, None, None, 1)
        cas_login_param.lt = lt
        cas_login_param._eventId = event_id
        cas_login_param.execution = execution
        cas_login_param.submit = submit
        return cas_login_param, cookies_jsessionid_value


def get_jsessionid(url):
    """
        获取jsessionid cookie
       @author xingguo
       @date 1/14/2019 4:29 PM
       @since 1.0.0
    """
    cookie_list = get_cookie(url)
    for cookie in cookie_list:
        cookie_name = cookie.name
        if cookie_name is not None and cookie_name == "JSESSIONID":
            return cookie


def computeMD5hash(my_string):
    # md5加密
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


def send_login_post(login_url, cas_login_param):

    # 使用urlencode方法转换标准格式
    post_data = parse.urlencode(cas_login_param.__dict__).encode('utf-8')
    # 提交参数发送登录请求
    headers["Cookie"] = "OUTFOX_SEARCH_USER_ID_NCOO=2139139465.580414"
    # request_request = request.Request(url=login_url, data=post_data, headers=headers)
    # read = request_request.read()
    # detect = chardet.detect(read)
    # # 读取信息并解码
    # html = read.decode(detect["encoding"], "ignore")
    # TODO: 登录失败
    # print(str(html))
    # 使用requests发送请求
    response = requests.post(url=login_url, data=post_data, headers=headers)
    response_headers = response.headers
    if response_headers is not None:
        for key in response_headers:
            value = response_headers[str(key)]
            if value is not None:
                print(str(key) + ":" + str(value))
    cookies = response.cookies
    if cookies is not None:
        for cookie in cookies:
            print(type(cookie))
            print(cookie.__dict__.values())

def send_logout():
    """
       登出
       @author xingguo
       @date 1/14/2019 1:49 PM
       @since 1.0.0
    """
    logout_url = "http://sso.test.tthunbohui.com/logout"
    request.urlopen(logout_url)


def simulation_cas_login(login_url, text_path):
    """
       模拟cas-server 4.0.0登录
       1: get请求登录地址,获取页面中的
       <input type="hidden" name="lt" value="LT-1342-73Dq7GeYM1d2dqVusKY9b04b1JdyFf-cas01.example.org" />
         <input type="hidden" name="execution" value="e2s1" />
         <input type="hidden" name="_eventId" value="submit" />
         三个标签的value值存储
       2: 使用登录账号和密码登录和上述参数组装提交数据
         username=18000000000&password=e10adc3949ba59abbe56e057f20f883e&vcode=1&lt=LT-1343-qe26ccbvVDvgnzUBdYP62PDZCRwvkh-cas01.example.org&execution=e1s1&_eventId=submit&submit=%E7%99%BB%E5%BD%95
        3: 获取jsessionid，并重新组装请求登陆地址 +；jsessionid= 调用登录地址发送post请求提交参数
       4：从返回headers中找到location获取st，并发送get请求
       5：获取st后换取session数据
       @author xingguo
       @date 1/11/2019 9:04 PM
       @since 1.0.0
    """
    # 登出
    send_logout()
    # 获取登录所需参数
    cas_login_param, jsessionid = list_cas_arg(login_url)
    cas_login_param.username = "18000000000"
    cas_login_param.password = computeMD5hash("123456")
    # 发送登录请求
    send_login_post(login_url + ";jsessionid=" + str(jsessionid), cas_login_param)


simulation_cas_login(url, "cookie.text")
