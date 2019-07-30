import scrapy
from jinsa.items import JinsaItem


class JinsaSpider(scrapy.Spider):
    name = "jinsa"
    allowed_domains = ['oxmo.cn']
    start_urls = [
        'https://www.oxmo.cn/'
    ]

    def parse(self, response):
        jin_urlss = response.xpath('//div[@class="lower"]')
        jin_urls = jin_urlss.xpath('//a/@href')
        for jin_url in jin_urls:
            yield response.follow(jin_url, callback=self.parse_next)

        # urls = response.xpath('//h1[@class="entry-title"]/a/@href')
        # for url in urls:
        #     yield response.follow(url, callback=self.parse_details)
        # if next_url:

    def parse_next(self,response):
        next_url = response.xpath('//link[@rel="next"]/@href').extract_first()
        urls = response.xpath('//h1[@class="entry-title"]/a/@href')
        for url in urls:
            yield response.follow(url, callback=self.parse_details)
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse_next)


    def parse_details(self,response):
        title = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        url = response.url
        article = response.xpath('//p[@class="entry-census"]/text()').extract_first()
        item = JinsaItem()
        item['title'] = title
        item['url'] = url
        item['article'] = article
        print(item)
        yield item

