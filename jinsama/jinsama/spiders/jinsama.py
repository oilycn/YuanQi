import scrapy
from jinsama.items import JinsamaItem

class JinSpider(scrapy.Spider):
	name = "jinsama"
	# allowed_domains = ['haha56.net']
	start_urls = [
		'http://www.haha56.net/'
	]

	def parse(self, response):
		topmenu = response.xpath('*//div[@class="topmenu cbody"]/ul/li')
		del topmenu[0:3]
		# print (topmenu)
		for data in topmenu:
			urls = data.xpath('./a/@href').extract_first()
			j_url = "http://www.haha56.net" + urls
			# print(j_url)
			yield scrapy.Request(j_url, callback=self.parse_url)

	def parse_url(self,response):
		print(response.url)
		item = JinsamaItem ()
		item['class_h'] = response.xpath ('//div[@class="placenav"]/a[2]/text()').extract_first ()
		datas = response.xpath('//div[@class="newslist"]/dl/dt/a/@href').extract()
		jin = response.xpath ('//a[contains(text(),"下一页")]/@href').extract_first ()
		for data in datas:
			if data.startswith('/'):
				url = "http://www.haha56.net" + data
			else:
				url = data
			yield scrapy.Request(url,meta={'item':item},callback=self.parse_details)
		if jin is not None:
			base_url = response.xpath ('//div[@class="placenav"]/a[2]/@href').extract_first ()
			next_urls = response.xpath ('//a[contains(text(),"下一页")]/@href').extract_first ()
			if base_url.startswith ('http'):
				next_url = base_url + next_urls
			else:
				next_url = "http://www.haha56.net" + base_url + next_urls
			yield scrapy.Request (next_url, callback=self.parse_url)


	def parse_details(self,response):
		item = response.meta['item']
		title = response.xpath('//div[@class="newsview"]/*[@class="title"]/text()').extract_first()
		url = response.url
		# article = response.css('.content').xpath('string(.)').extract_first()
		article = response.css ('.content').extract_first ()
		item['title'] = title
		item['url'] = url
		item['article'] = article
		# print(item)
		yield item
