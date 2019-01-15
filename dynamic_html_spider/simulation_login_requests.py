# -*- coding: UTF-8 -*-
"""
    模拟登录使用request库
   @author xingguo
   @date 1/14/2019 5:45 PM
   @since 1.0.0
"""
import hashlib
from urllib import parse

import requests
from bs4 import BeautifulSoup

from dynamic_html_spider.cas_login_param import CasLoginParam

url = "http://sso.test.tthunbohui.com/login"

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
    html = response.text
    # 获取jsessionId
    cookies = response.cookies
    cookies_jsessionid_value = cookies["JSESSIONID"]
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
        cas_login_param = CasLoginParam(None, None, None, None, None, None, 1)
        cas_login_param.lt = lt
        cas_login_param._eventId = event_id
        cas_login_param.execution = execution
        cas_login_param.submit = submit
        return cas_login_param, cookies_jsessionid_value


def computeMD5hash(my_string):
    # md5加密
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


def send_login_post(login_url, cas_login_param):
    # 使用urlencode方法转换标准格式
    post_data = parse.urlencode(cas_login_param.__dict__).encode('utf-8')
    # 使用requests发送请求
    response = requests.post(url=login_url, data=post_data, headers=headers)
    response_headers = response.headers
    if response_headers is not None:
        for key in response_headers:
            value = response_headers[str(key)]
    cookies = response.cookies
    tgt = ""
    if cookies is not None:
        for cookie in cookies:
            if cookie is not None and str(cookie.name) == "CASTGC":
                tgt = str(cookie.value)
    text = response.text
    soup = BeautifulSoup(text, "html.parser")
    href = soup.find("a").get("href")
    return href, tgt


def send_logout():
    """
       登出
       @author xingguo
       @date 1/14/2019 1:49 PM
       @since 1.0.0
    """
    logout_url = "http://sso.test.tthunbohui.com/logout"
    requests.get(logout_url)


def simulation_cas_login(login_url):
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
    bopshref, tgt = send_login_post(login_url + ";jsessionid=" + str(jsessionid), cas_login_param)
    headers["Cookie"] = "CASTGC=" + tgt + ";JSESSIONID=" + str(jsessionid)
    bops_response = requests.get(bopshref, allow_redirects=False)
    bops_login_url = bops_response.headers["Location"]
    # 根据TGT换取ST
    response_bops_st = requests.get(url=bops_login_url, headers=headers, allow_redirects=False)
    st_redirect_url = response_bops_st.headers["Location"]
    # 通过ST获取session信息
    session_response = requests.get(st_redirect_url, allow_redirects=False)
    response_cookie_list = session_response.cookies
    for cookie in response_cookie_list:
        if cookie is not None and str(cookie.name) == "SESSION":
            headers["Cookie"] = "SESSION=" + str(cookie.value)
    final_url = session_response.headers["Location"]
    requests.get(final_url, headers=headers)


simulation_cas_login(url)
