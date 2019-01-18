# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
from dynamic_html_spider.selenium_test.selenium_test import open_browser

"""
   xpath 使用
   @author xingguo
   @date 1/17/2019 5:50 PM 
   @since 1.0.0 
"""


def test_xpath():
    """
       xpath 常用功能
       @author xingguo
       @date 1/17/2019 5:55 PM
       @since 1.0.0
    """
    # 以百度文库为例子
    url = "https://wenku.baidu.com/view/aa31a84bcf84b9d528ea7a2c.html"
    # 打开浏览器
    browser = open_browser(url)

