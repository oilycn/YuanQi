import scrapy
import json
from cili.items import CiliItem

class CiliSpider(scrapy.Spider):
	name = 'cili' #scrapy crawl cili
	keyword = "av"
	a = 1
	#allowed_domains = ['taobao.com']
	url = 'http://bt.cywacg.com/api/search?source=种子搜&keyword=%s&sort=time&page=%d'

	def start_requests(self):
		yield scrapy.Request(self.url % (self.keyword, self.a), callback=self.parse)

	def parse(self, response):
		y = 0
		datas = json.loads(response.body_as_unicode())
		results = datas['data']['results']
		for result in results:
			y = y + 1
			item = CiliItem()
			item['name'] = result['name']
			item['formatSize'] = result['formatSize']
			item['date'] = result['date']
			item['hot'] = result['hot']
			item['detailUrl'] = result['detailUrl']
			item['magnet'] = result['magnet']
			yield item
			# print(item)
			# print(y)

		if y < 15:
			num = (self.a - 1) * 15 + y
			print ( '磁力【' + self.keyword + '】: ' + '已采集' + str ( self.a ) + '页' + '，总数据 ：' + str ( num ) + '条' )
			self.crawler.engine.close_spider ( self, '已爬取所有信息！' )
		else:
			num = self.a * 15
			print ( '磁力【' + self.keyword + '】: ' + '已采集' + str ( self.a ) + '页' + '，总数据 ：' + str ( num ) + '条' )
			self.a = self.a + 1
			yield scrapy.Request ( self.url % (self.keyword, self.a), callback=self.parse )