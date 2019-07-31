import scrapy
import json
from taobao.items import TaobaoItem


class TaobaoSpider(scrapy.Spider):
	name = 'taobao' #scrapy crawl taobao
	keyword = "宾格瑞"
	a = 0
	allowed_domains = ['taobao.com']
	url = 'https://s.taobao.com/search?q=%s&bcoffset=0&ntoffset=6&p4ppushleft=1&s=%d'

	def start_requests(self):
		yield scrapy.Request(self.url % (self.keyword, self.a * 44), callback=self.parse)


	def parse(self, response):
		y = 0
		p = 'g_page_config = ({.*?});'
		g_page_config = response.selector.re(p)[0]
		g_page_config = json.loads(g_page_config)
		auctions = g_page_config['mods']['itemlist']['data']['auctions']
		# g_page_configs = response.selector.re(r'g_page_config = ({.*?});')
		totalPage = response.selector.re(r'"totalPage":(.*?),')[0]
		for auction in auctions:
			y = y + 1
			item = TaobaoItem()
			item['title'] = auction['raw_title']
			item['price'] = auction['view_price']
			item['nick'] = auction['nick']
			item['sales'] = auction['view_sales']
			item['loc'] = auction['item_loc']
			item['detail_url'] = auction['detail_url']
			if item['detail_url'].startswith('//'):
				item['detail_url'] = 'https:' + item['detail_url']
				yield item

		PageNow = self.a + 1
		if str(PageNow) >= totalPage:
			num = self.a * 44 + y - 4
			print('淘宝【' + self.keyword + '】: ' + '已采集' + str(self.a + 1) + '页' + '，总数据 ：' + str(num) + '条')
			self.crawler.engine.close_spider(self, '已爬取所有信息！')
		else:
			num = self.a  * 44 + y - 4
			print('淘宝【' + self.keyword + '】: ' + '已采集' + str(self.a + 1) + '页' + '，总数据 ：' + str(num) + '条')
			self.a = self.a + 1
			yield scrapy.Request(self.url % (self.keyword, self.a * 44), callback=self.parse)