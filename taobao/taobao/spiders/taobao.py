import scrapy
import json
from taobao.items import TaobaoItem


class TaobaoSpider(scrapy.Spider):
	name = "taobao"
	a = 1
	allowed_domains = ['taobao.com']
	start_url = 'https://s.taobao.com/search?q='
	keywords = '口红'

	def start_requests(self):
		for i in range(99):  # 页数
			url = self.start_url + self.keywords + '&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s=' + str(i * 44)
			yield scrapy.FormRequest(url=url, callback=self.parse)

	def parse(self, response):
		p = 'g_page_config = ({.*?});'
		g_page_config = response.selector.re(p)[0]
		g_page_config = json.loads(g_page_config)
		auctions = g_page_config['mods']['itemlist']['data']['auctions']
		for auction in auctions:
			item = TaobaoItem()
			item['title'] = auction['raw_title']
			item['price'] = auction['view_price']
			item['nick'] = auction['nick']
			item['sales'] = auction['view_sales']
			item['loc'] = auction['item_loc']
			item['detail_url'] = auction['detail_url']
			yield item
		print('淘宝【' + self.keywords + '】: ' + '已采集第' + str(self.a) + '页')
		self.a = self.a + 1