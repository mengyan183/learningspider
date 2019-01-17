# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
import unittest

from dynamic_html_spider.selenium_test.selenium_test import open_browser, personification_post

"""
    unittest 测试case编写
   @author xingguo
   @date 1/17/2019 2:22 PM 
   @since 1.0.0 
"""


class TestSelenium(unittest.TestCase):

    def test_open_url(self):
        url = "http://www.baidu.com"
        open_browser(url)

    def test_personification_post(self):
        personification_post()
