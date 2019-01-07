# -*- coding: UTF-8 -*-
import ssl
import sys
import time
from urllib import request

from bs4 import BeautifulSoup
from pip import __main__

# 请求https网址 将SSL强制身份验证关闭
ssl._create_default_https_context = ssl._create_unverified_context
'''
 * 爬取静态页面(笔趣阁),并将文件保存到本地
 * @author guoxing
 * @date 2019-01-07 11:47 AM
 * @since 2.0.0
'''
if __name__=='__main__':
    # 创建一个新的文件或打开已存在的文件(覆写操作) 'w'       open for writing, truncating the file first
    file = open('一念永恒.txt', 'w', encoding='utf-8')
    # 新增变量(一念永恒章节列表访问网址)
    yinianyongheng_url="https://www.biqukan.com/1_1094/"
    # 定义head对象
    head={}
    # 添加UA 属性
    head['User-Agent']="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    head['DNT']="1"
    # 新增cookie属性,需要首先从浏览器获取完整的cookie信息
    head['Cookie']="fikker-iMor-eTMM=7PEHLZmI1TElARGhoxUB9RMVwxYHuP9R; fikker-iMor-eTMM=7PEHLZmI1TElARGhoxUB9RMVwxYHuP9R; bcolor=; font=; size=; fontcolor=; width=; fikker-GVQV-QnJf=CDAvyOQT7O5Xon5MST3Ps4QLg4EOeNWJ; fikker-GVQV-QnJf=CDAvyOQT7O5Xon5MST3Ps4QLg4EOeNWJ"
    # 如果不需要传递headers等特殊数据,只需要发起一个单独的url http请求,可以写为response = request.urlopen(url地址)
    # 创建request请求,并传递url和headers
    yinianyongheng_req=request.Request(url=yinianyongheng_url,headers=head)
    # 发送请求,并返回response响应
    yinianyongheng_response=request.urlopen(yinianyongheng_req)
    # 获取响应结果的字节数组,并将字节数组解码为gbk编码格式的文字
    yinianyongheng_html=yinianyongheng_response.read().decode('gbk','ignore')
    # 使用beautifulSoup解析html
    listmain_soup=BeautifulSoup(yinianyongheng_html,'html.parser')
    # 获取该页面中的所有class为listman的div标签
    chapters=listmain_soup.find_all('div',class_='listmain')
    # 解析指定的页面标签数据,获取到章节菜单列表数据
    download_soup=BeautifulSoup(str(chapters),'html.parser')
    # 获取总章节数量
    numbers = (len(download_soup.dl.contents) - 1) / 2 - 8
    index = 1
    begin_flag=False
    for child in download_soup.dl.children:
        # 获取所有dl标签下的标签
        if child != '\n':
            if child.string == "《一念永恒》正文卷":
                begin_flag = True
            if begin_flag == True and child.a != None:
                # 获取该标签中的a超链接标签中 href属性值,拼接具体章节访问地址
                download_url = "https://www.biqukan.com" + child.a.get('href')
                # 章节名称
                download_name = child.string
                # 打印章节名和访问地址
                print(download_name + " : " + download_url)
                # 延时一秒
                time.sleep(1)
                # 创建访问页面的request
                download_req=request.Request(url=download_url,headers=head)
                # 发送请求
                download_response=request.urlopen(download_req)
                # 解析响应结果
                download_html=download_response.read().decode('gbk','ignore')
                soup_texts=BeautifulSoup(download_html,'html.parser')
                texts=soup_texts.find_all(id='content',class_='showtxt')
                soup_text=BeautifulSoup(str(texts),'html.parser')
                write_flag=True
                file.write(download_name+'\n\n')
                # 替换所有空格
                for each in soup_text.div.text.replace('\xa0', ''):
                    if each == 'h':
                        write_flag = False
                    if write_flag == True and each != ' ':
                        file.write(each)
                    if write_flag == True and each == '\r':
                        file.write('\n')
                file.write('\n\n')
                # 打印爬取进度
                print("已下载:%.3f%%" % float(index / numbers)*100 + '\r')
                # sys.stdout.flush()
                index += 1
    file.close()
    # 退出主进程
    sys.exit(__main__._main())