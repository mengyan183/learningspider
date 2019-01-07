# -*- coding: UTF-8 -*-
import sys
import time

from bs4 import BeautifulSoup
from urllib import request
from pip import __main__
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
if __name__=='__main__':
    file = open('一念永恒.txt', 'w', encoding='utf-8')
    yinianyongheng_url="https://www.biqukan.com/1_1094/"
    head={}
    head['User-Agent']="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    head['DNT']="1"
    head['Cookie']="fikker-iMor-eTMM=7PEHLZmI1TElARGhoxUB9RMVwxYHuP9R; fikker-iMor-eTMM=7PEHLZmI1TElARGhoxUB9RMVwxYHuP9R; bcolor=; font=; size=; fontcolor=; width=; fikker-GVQV-QnJf=CDAvyOQT7O5Xon5MST3Ps4QLg4EOeNWJ; fikker-GVQV-QnJf=CDAvyOQT7O5Xon5MST3Ps4QLg4EOeNWJ"
    yinianyongheng_req=request.Request(url=yinianyongheng_url,headers=head)
    yinianyongheng_response=request.urlopen(yinianyongheng_req)
    yinianyongheng_html=yinianyongheng_response.read().decode('gbk','ignore')
    listmain_soup=BeautifulSoup(yinianyongheng_html,'html.parser')
    chapters=listmain_soup.find_all('div',class_='listmain')
    download_soup=BeautifulSoup(str(chapters),'html.parser')
    numbers = (len(download_soup.dl.contents) - 1) / 2 - 8
    index = 1
    begin_flag=False
    for child in download_soup.dl.children:
        if child != '\n':
            if child.string == "《一念永恒》正文卷":
                begin_flag = True
            if begin_flag == True and child.a != None:
                download_url = "https://www.biqukan.com" + child.a.get('href')
                download_name = child.string
                print(download_name + " : " + download_url)
                # 延时一秒
                time.sleep(1)
                download_req=request.Request(url=download_url,headers=head)
                download_response=request.urlopen(download_req)
                download_html=download_response.read().decode('gbk','ignore')
                download_name=child.string
                soup_texts=BeautifulSoup(download_html,'html.parser')
                texts=soup_texts.find_all(id='content',class_='showtxt')
                soup_text=BeautifulSoup(str(texts),'html.parser')
                write_flag=True
                file.write(download_name+'\n\n')
                for each in soup_text.div.text.replace('\xa0', ''):
                    if each == 'h':
                        write_flag = False
                    if write_flag == True and each != ' ':
                        file.write(each)
                    if write_flag == True and each == '\r':
                        file.write('\n')
                file.write('\n\n')
                # 打印爬取进度
                print("已下载:%.3f%%" % float(index / numbers) + '\r')
                # sys.stdout.flush()
                index += 1
    file.close()
    sys.exit(__main__._main())