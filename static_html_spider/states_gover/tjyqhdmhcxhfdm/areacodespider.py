# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
import re
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


# 中国国家统计局统计用区划代码和城乡划分代码请求地址
base_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"

# headers
headers = {}
headers["Cookie"] = "AD_RS_COOKIE=20081945; _trs_uv=jqn5fkaf_6_feew; _trs_ua_s_1=jqnif7cc_6_5ipjs"
headers[
    "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
headers["Referer"] = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/"


def province_national_bureau_of_statistics_of_china():
    """
        爬取中国国家统计局区域划分代码
       @author xingguo
       @date 1/8/2019 4:47 PM
       @since 1.0.0
    """
    url = base_url + "index.html"

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
    province_list = []
    # 解析所有a标签数据
    for city_a in a_list:
        # 获取省份名称
        city_name = city_a.text
        # 获取a标签的href属性
        href = city_a.get("href")
        # 获取访问子级区域的url地址
        child_url = base_url + str(href)
        # 获取当前区域的code
        city_code = str(href)[0:str(href).find(".html")]
        left_zero = 6 - len(city_code)
        # 转换为6位标准格式areacode
        left_zeros = "0" * left_zero
        city_code += left_zeros
        area = Area(city_name, city_code, 0, child_url)
        # print(area.__dict__.values())
        province_list.append(area)
    return province_list


# 获取所有省级区域数据
province_list = province_national_bureau_of_statistics_of_china()


def list_child_area(area):
    """
        :param area 父级区域数据
        :returns 当前区域下的所有子级区域数据
        采用递归的方法遍历区域数据,直到最终子集区域
       @author xingguo
       @date 1/10/2019 1:42 PM
       @since 1.0.0
    """
    # 初始化区域字典(集合)
    area_list = []
    if area is None or type(area) is not Area:
        return area_list
    # 当前区域的code
    parent_code = area.code
    # 子区域请求地址
    child_url = area.child_url
    if child_url is None:
        return area_list;
    url = child_url

    # 创建request
    request_request = request.Request(url=url, headers=headers)
    try:
        # 发送请求
        response = request.urlopen(request_request)
        # 解析响应
        read = response.read()
        detect = chardet.detect(read)
        # 读取信息并解码
        html = read.decode(detect["encoding"],'ignore')
        # 解析html
        soup = BeautifulSoup(html, "html.parser")
        # 获取所有 class="citytr" 的tr标签
        city_tr_list = soup.select("tr[class$='tr']")
        for city_tr in city_tr_list:
            city_tr_beautiful_soup = BeautifulSoup(str(city_tr), "html.parser")
            # 获取所有的a标签
            city_tr_td_a_list = city_tr_beautiful_soup.find_all("a")

            # 如果当前标签下没有a标签,说明当前区域是最后一级
            if not city_tr_td_a_list or city_tr_td_a_list is None:
                city_tr_td_list = city_tr_beautiful_soup.find_all("td")
                area_code = city_tr_td_list[0].text
                # 获取区域名称
                area_name = city_tr_td_list[-1].text
                child_url = None
                a = Area(area_name, area_code, parent_code, child_url)
                area_list.append(a)
                break
            else:
                # 获取最后一个a标签
                city_tr_td_a = city_tr_td_a_list[-1]
                # a标签href属性值
                a_href = city_tr_td_a.get("href")
                # 获取区域名称
                area_name = city_tr_td_a.text
                # 解析href中的区域code
                a_href_array = str(a_href).split("/")
                href = a_href_array[-1]
                pre_href = href[0:href.find(".html")]
                # 写出正则表达式 任意2个字符
                pattern = re.compile('.{2}')
                result = ' '.join(pattern.findall(pre_href))
                split_list = result.split(" ")
                pre = ""
                for i in range(len(split_list) - 1):
                    pre += split_list[i]+"/"
                index = str(href).find(".html")
                area_code = str(href)[0:index]
                length = len(area_code)
                if length < 6:
                    area_code += ((6 - length) * "0")
                child_url = base_url + pre + href
                a = Area(area_name, area_code, parent_code, child_url)
            if city_tr_td_a_list is not None:
                child_area_list = list_child_area(a)
                if child_area_list is not None:
                    area_list.extend(child_area_list)
            area_list.append(a)
    except EnvironmentError as e:
        print(url)

    return area_list


# 获取所有省级的子级数据
total_china_area_list = []
for province in province_list:
    if province is not None:
        child_area_list = list_child_area(province)
        if child_area_list is not None and child_area_list != []:
            total_china_area_list.append(child_area_list)

for area in total_china_area_list:
    if area is not None and type(area) == Area:
        print(area.__dict__.values())

