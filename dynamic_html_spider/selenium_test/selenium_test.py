# -*- coding: UTF-8 -*-
"""
Copyright 2019 [xingguo] All rights Reserved.
"""
import platform
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

"""
    selenium 测试
   @author xingguo
   @date 1/16/2019 1:47 PM 
   @since 1.0.0 
"""


def get_path():
    """
        根据不同操作系统返回不同的webdriver相对路径
       @author xingguo
       @date 1/17/2019 2:29 PM
       @since 1.0.0
    """
    platform_name = sys.platform
    print("platform:" + str(platform_name))
    system = platform.system()
    print("system:" + str(system))
    path = ""
    if system is not None:
        s = str(system)
        if s == "Windows":
            path = "windows/chromedriver.exe"
        if s == "Linux":
            path = "linux/chromedriver"
        if s == "Darwin":
            path = "macos/chromedriver"
    return path


def open_browser(url):
    """
       :param url:请求地址
       打开chrome浏览器访问指定地址
       @author xingguo
       @date 1/17/2019 2:26 PM
       @since 1.0.0
    """
    # 配置chromedriver路径
    # https://sites.google.com/a/chromium.org/chromedriver/downloads , 下载运行系统指定的文件到当前文件所在目录下
    # 获取chromediver相对路径
    argument = 'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/70.0.3538.77 Safari/537.36"'
    open_browser(url=url, argument=argument)


def open_browser(url, argument):
    path = get_path()
    if path is not None and path != "":
        options = webdriver.ChromeOptions()
        # 添加useragent
        options.add_argument(argument)
        chrome = webdriver.Chrome(path)
        chrome.get(url)
        return chrome


def personification_post():
    """
        模拟人工操作打开python官网并执行搜索
       @author xingguo
       @date 1/17/2019 2:33 PM
       @since 1.0.0
    """
    url = "http://www.python.org"
    # 打开浏览器并返回
    browser = open_browser(url)
    assert "Python" in browser.title
    page = browser.find_elements_by_xpath("//div[@class='page']")
    if page is not None and type(page) == "list" and len(page) > 0:
        # 拖动到可见的元素去
        browser.execute_script('arguments[0].scrollIntoView();', page[-1])
        # 执行鼠标点击事件
        page.click()
    # 查找p元素
    elem = browser.find_element_by_name("q")
    # 单个元素查找,使用selenium.webdriver.common.by.By 决定不同的元素类型
    elem = browser.find_element(By.NAME, "q")
    # 批量查找指定元素
    # elems = browser.find_elements(By.NAME, "q")
    # 输入相关字符
    elem.send_keys("python")
    # 执行回车键
    elem.send_keys(Keys.RETURN)
    # 打印网页页面代码
    print(browser.page_source)
