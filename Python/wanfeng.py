#-*- coding:utf-8 -*-

import requests #导入requests包
import re

url = "http://oxmo.cn"
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
res = requests.get(url,headers=headers)

def pages_text(mydata):
    # 分页链接获取
    pages = re.findall(r'<div id="pagination"><a href="(.*?)">Previous</a></div>',mydata,re.S)
    return pages


def article_data(mydata):
    # 获取文章标题和链接
    article = re.findall(r'<div class="post-date">(.*?)<div class="post-meta">',mydata,re.S)

    for data in article:
        title = re.findall(r'<h3>(.*?)</h3>',data,re.S)
        title_url = re.findall(r'<a href="(.*?)"',data,re.S)
        print(title[0])
        print(title_url[0])
    try:
        ress = requests.get(pages_text(mydata)[0],headers=headers)
        article_data(ress.text)
    except:
        print('完成所有数据的爬虫！')

article_data(res.text)


