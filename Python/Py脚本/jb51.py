import requests
from bs4 import  BeautifulSoup
import csv

url = "https://www.jb51.net/list/list_206_1.htm"
filename = 'jb51_Delphi'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
}

# 1. 创建文件对象 
f = open(filename + '.csv','w',encoding='utf-8',newline="") # newline 解决空行问题
# 2. 基于文件对象构建 csv写入对象
csv_writer = csv.writer(f)
# 3. 构建列表头
csv_writer.writerow(["标题","链接"])

def main(url_):
    r = requests.get(url_,headers)
    r.encoding = 'gb18030' 
    soup = BeautifulSoup(r.text,'lxml')
    article = soup.findAll('div',class_="artlist clearfix")[0].findAll('a',target="_blank")
    next_page = 'https://www.jb51.net' + soup.find('a',title="下页")['href']
    last_page = 'https://www.jb51.net' + soup.find('a',title="末页")['href']
    for i in article:
        # 4. 写入csv文件内容
        csv_writer.writerow([i['title'],'https://www.jb51.net' + i['href']])
        # print(i['title'])
        # print('https://www.jb51.net' + i['href'])
    if last_page != next_page:
        main(next_page)
    else:
        # 5. 关闭文件
        f.close()
        print(filename + '数据爬虫已完成！')
        exit()

if __name__ == '__main__':
    main(url)