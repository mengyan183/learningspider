# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
from enum import Enum

"""
    中国民政部县以上(包含县)区划代码爬取
   @author xingguo
   @date 1/11/2019 11:46 AM 
   @since 1.0.0 
"""


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


def mca_area_code_spider(Area):
    """
        民政部行政区域爬取
        TODO:
       @author xingguo
       @date 1/11/2019 11:52 AM
       @since 1.0.0
    """
    area_list = []
    return area_list
