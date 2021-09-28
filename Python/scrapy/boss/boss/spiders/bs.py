# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from boss.items import BossItem

class BsSpider(CrawlSpider):
    name = 'bs'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101200100/?page=1&ka=page-next']

    rules = (
        Rule(LinkExtractor(allow=r'job_detail/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = BossItem()
        try:
            item["title"]=response.xpath('//div[@class="name"]/h1/text()').extract()[0]
            #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
            #item['name'] = response.xpath('//div[@id="name"]').get()
            #item['description'] = response.xpath('//div[@id="description"]').get()
            print(item)
            yield item
        except Exception as e:
            print(e)