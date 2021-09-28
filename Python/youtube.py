from lxml import etree
import requests

url = 'https://www.youtube.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'
}
r = requests.get(url, headers=headers)

html = etree.HTML(r.text)
# html_data = html.xpath('//*[@id="video-title"]')
html_data = html.xpath('//h3[@class="style-scope ytd-rich-grid-media"]')
for i in html_data:
    print(i.text)
