# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
from urllib import request

import chardet
from bs4 import BeautifulSoup

"""
    中国国家行政区域划分代码
   @author xingguo
   @date 1/8/2019 10:48 AM 
   @since 1.0.0 
"""


class Area:
    """
    区域(省份/市区/县/乡)
   @author xingguo
   @date 1/8/2019 11:07 AM
   @since 1.0.0
    """

    def __init__(self, name, code, parent_code, child_url):
        # 名称
        self.name = name
        # 区域code
        self.code = code
        # 父级区域code
        self.parent_code = parent_code
        # 子区域访问URL
        self.child_url = child_url


def province_national_bureau_of_statistics_of_china():
    """
        爬取中国国家统计局区域划分代码
       @author xingguo
       @date 1/8/2019 4:47 PM
       @since 1.0.0
    """
    # 中国国家统计局统计用区划代码和城乡划分代码请求地址
    base_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"
    url = base_url + "index.html"
    # headers
    headers = {}
    headers["Cookie"] = "AD_RS_COOKIE=20081945; _trs_uv=jqn5fkaf_6_feew; _trs_ua_s_1=jqnif7cc_6_5ipjs"
    headers[
        "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    headers["Referer"] = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/"

    # 创建request
    request_request = request.Request(url=url, headers=headers)
    # 发送请求
    response = request.urlopen(request_request)
    # 解析响应
    read = response.read()
    detect = chardet.detect(read)
    # 读取信息并解码
    html = read.decode(detect["encoding"])
    # 解析html
    soup = BeautifulSoup(html, "html.parser")
    # 获得到所有的tr标签
    find_all_tr = soup.find_all('tr', class_="provincetr")
    # 解析标签内数据
    beautiful_soup_tr = BeautifulSoup(str(find_all_tr), "html.parser")
    # 所有a标签
    a_list = beautiful_soup_tr.find_all('a')
    # 解析所有a标签数据
    for city_a in a_list:
        # 获取省份名称
        city_name = city_a.string
        href = city_a.href
        # 获取访问子级区域的url地址
        child_url = base_url.join(href)
        city_code = href.split(0, href.find(".html"))
        left_zero = 6 - len(city_code)
        # 转换为6位标准格式areacode
        city_code = city_code.join("0", left_zero)
        area = Area(city_name, city_code, 0, child_url)
        # TODO : 
