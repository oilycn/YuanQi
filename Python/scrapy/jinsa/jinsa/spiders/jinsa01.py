import scrapy
from jinsa.items import JinsaItem
# import ssl #解决https
# ssl._create_default_https_context = ssl._create_unverified_context #解决https
# from fake_useragent import UserAgent
# ua = UserAgent()

class JinsaSpider(scrapy.Spider):
    name = "jinsa01"
    allowed_domains = ['oxmo.cn']
    start_urls = [
        'https://www.oxmo.cn/article/'
    ]

    def parse(self, response):
        next_url = response.xpath('//link[@rel="next"]/@href').extract_first()
        urls = response.xpath('//h1[@class="entry-title"]/a/@href')
        for url in urls:
            yield response.follow(url, callback=self.parse_details)
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_details(self,response):
        title = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        url = response.url
        article = response.xpath('//div[@class="entry-content"]').extract_first()
        item = JinsaItem()
        item['title'] = title
        item['url'] = url
        item['article'] = article
        print(item)
        yield item

