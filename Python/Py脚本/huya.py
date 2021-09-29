from bs4 import BeautifulSoup
import requests

url = 'http://www.huya.com/l'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
}

def GetTitleAndUrl(url_):
    # 获取直播间标题和链接
    r = requests.get(url_, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    # html_data = html.xpath('//*[@id="video-title"]')
    next_page = soup.find('div',id="js-list-page")['data-pages']
    print(next_page)
    html_data = soup.find_all('li',class_="game-live-item")
    # print(html_data)
    for i in html_data:
        zhibo = i.find('a',class_="title")
        print(zhibo['title'])
        print(zhibo['href'])

if __name__ == '__main__':
    GetTitleAndUrl(url)