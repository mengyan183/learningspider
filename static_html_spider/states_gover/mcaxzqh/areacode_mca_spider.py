# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
from enum import Enum
from urllib import request

import chardet
import mysql.connector
from bs4 import BeautifulSoup
import pymysql
"""
    中国民政部县以上(包含县)区划代码爬取
   @author xingguo
   @date 1/11/2019 11:46 AM 
   @since 1.0.0 
"""

# headers
# headers = {}
# headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"


class AreaLevel(Enum):
    """
        中国国家行政区域级别划分
       @author xingguo
       @date 1/11/2019 11:04 AM
       @since 1.0.0
    """
    # 国家
    NATION = 0
    # 省级行政区
    PROVINCIAL = 1
    # 地级行政区
    PREFECTURE = 2
    # 县级行政区
    COUNTRY = 3
    # 乡级行政区
    TOWNSHIP = 4
    # 村级行政区
    VILLAGE = 5


class Area:
    """
        县级(包含县)以上行政区域划分
       @author xingguo
       @date 1/11/2019 11:48 AM
       @since 1.0.0
    """

    def __init__(self, name, code, parent_code, level):
        # 名称
        self.name = name
        # 区域code
        self.code = code
        # 父级区域code
        self.parent_code = parent_code
        # 级别(0:全国,1:省级行政区,2:地级行政区,3:县级行政区) https://zh.wikipedia.org/wiki/中华人民共和国行政区划
        self.level = level


def mca_area_code_spider():
    """
        民政部行政区域爬取
       @author xingguo
       @date 1/11/2019 11:52 AM
       @since 1.0.0
    """
    area_list = []
    url = "http://www.mca.gov.cn/article/sj/xzqh/2018/201804-12/20181101021046.html"
    # TODO : 代理不生效
    # #这是代理IP, https://www.xicidaili.com/
    # proxy = {'http':'111.181.70.143:9999'}
    # #创建ProxyHandler
    # proxy_support = request.ProxyHandler(proxy)
    # #创建Opener
    # opener = request.build_opener(proxy_support)
    # #添加User Angent
    # opener.addheaders = [headers]
    # #安装OPener
    # request.install_opener(opener)

    response = request.urlopen(url)
    # 解析响应
    read = response.read()
    detect = chardet.detect(read)
    # 读取信息并解码
    html = read.decode(detect["encoding"], "ignore")
    # 解析html
    soup = BeautifulSoup(html, "html.parser")
    tr_list = soup.find_all("tr")
    for tr in tr_list:
        tr_soup = BeautifulSoup(str(tr), "html.parser")
        td_list = tr_soup.find_all("td")
        if td_list is not None and len(td_list) > 2:
            area_code = td_list[1].text
            area_name = td_list[2].text
            if area_code is not None and area_name is not None and str(area_code) and str(area_name) and str(
                    area_code).isdigit():
                area = Area(area_name, area_code, None, None)
                area_list.append(area)
    return area_list


over_country_area_list = mca_area_code_spider()
print(len(over_country_area_list))

# 订正数据,对数据进行分级处理; 县和县以上数据area_code全为6位纯数字;省级行政区XX0000格式,地级行政区XXXX00格式,县级行政区XXXXXX格式
fix_area_code_list = []
# 元组数据
tuple_fix_area_code_list = []
# 创建sql连接
# TODO:请修改sql连接方式
my_local_db =pymysql.connect( host="test.dmp.mysqlm.jhops.club",
                         port=3309,
                         user="root",
                         passwd="",
                         database="dmp_base",charset="utf8")

# TODO:对于直辖市缺少市辖区数据
for area in over_country_area_list:
    code = area.code
    # 省级行政区
    if str(code).endswith("0000"):
        area.level = AreaLevel.PROVINCIAL.value
        area.parent_code = 0
        # 地级行政区
    elif str(code).endswith("00"):
        area.level = AreaLevel.PREFECTURE.value
        area.parent_code = str(code)[:2] + "0000"
    else:
        # 县级行政区
        area.level = AreaLevel.COUNTRY.value
        area.parent_code = str(code)[:4] + "00"
    print(area.__dict__.values().__str__())
    # tuple 将序列转换为元组
    tuple_fix_area_code_list.append(tuple(area.__dict__.values()))
    fix_area_code_list.append(area)

# 将数据保存到数据库
my_cursor = my_local_db.cursor()
my_cursor.execute("DROP TABLE IF EXISTS `area`;")
# 建表语句
create_table_sql = '''CREATE TABLE `area` (
    `area_id` int(5) unsigned NOT NULL AUTO_INCREMENT COMMENT '区域id',
    `area_name` varchar(255) NOT NULL DEFAULT '' COMMENT '区域名称',
    `area_code` int(12) unsigned zerofill NOT NULL DEFAULT '0' COMMENT '区域代码',
    `parent_code` int(12) unsigned zerofill NOT NULL DEFAULT '0' COMMENT '父级区域代码',
    `level` tinyint(1) unsigned zerofill NOT NULL DEFAULT '0' COMMENT '级别(0:全国,1:省级行政区,2:地级行政区,3:县级行政区,4:乡级行政区,5:村级行政区)',
    `use_status` tinyint(1) unsigned zerofill NOT NULL DEFAULT '0' COMMENT '启用禁用状态;0:启用,1:禁用',
    `del_flag` tinyint(1) unsigned zerofill NOT NULL DEFAULT '0' COMMENT '删除状态;0:未删除,1:已删除',
    PRIMARY KEY (`area_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='国家行政区域表';'''
my_cursor.execute(create_table_sql)
# 数据插入语句
sql = "INSERT INTO `area` (`area_name`, `area_code`, `parent_code`, `level`) VALUES (%s, %s, %s, %s)"
val = tuple_fix_area_code_list
print(val)
my_cursor.executemany(sql, val)
my_local_db.commit()
