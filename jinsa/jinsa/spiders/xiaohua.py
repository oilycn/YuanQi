import scrapy
from jinsa.items import JinsaItem
# import ssl #解决https
# ssl._create_default_https_context = ssl._create_unverified_context #解决https


class JinsaSpider(scrapy.Spider):
	name = "xixi"
	allowed_domains = ['haha56.net']
	start_urls = [
		'http://www.haha56.net/duanzi/'
	]

	def parse(self, response):
		jin_urlss = response.xpath('//div[@class="newslist"]')
		urls = jin_urlss.xpath('//dl/dt/a/@href')
		for url in urls:
			yield response.follow(url, callback=self.parse_details)

		next_url = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
		if next_url is not None:
			next_page = 'http://www.haha56.net/main/bxxh/' + next_url
			yield scrapy.Request(next_page,callback=self.parse)

	def parse_details(self,response):
		title = response.xpath('//div[@class="title"]/text()').extract_first()
		url = response.url
		article = response.xpath('//div[@class="content"]/text()').extract_first()
		item = JinsaItem()
		item['title'] = title
		item['url'] = url
		item['article'] = article
		print(item)
		yield item

