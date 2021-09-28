# -*- coding: utf-8 -*-
import scrapy
from job.items import JobItem
import re
from scrapy_redis.spiders import RedisSpider

class QcSpider(RedisSpider):
    name = 'qc'
    allowed_domains = ['51job.com']
    #start_urls = ['https://search.51job.com/list/180200,000000,0000,00,9,99,%2520,2,1.html']
    redis_key = "job"  # 这个名字随便写

    def parse(self, response):
        item=JobItem()
        elist=response.xpath('//*[@id="resultList"]//div[@class="el"]').extract()
        for i in range(0,len(elist)):
            el=elist[i]
            item['title']=re.findall('title="(.*?)"',el,re.S)[0]
            item['url'] = re.findall('href="(.*?)"',el,re.S)[0]
            item['company'] = re.findall('title="(.*?)"',el,re.S)[1]
            item['company_url'] = re.findall('href="(.*?)"',el,re.S)[1]
            item['loc'] = re.findall('<span class="t3">(.*?)</span>',el,re.S)[0]
            item['money'] = re.findall('<span class="t4">(.*?)</span>',el,re.S)[0]
            item['time'] = re.findall('<span class="t5">(.*?)</span>',el,re.S)[0]
            print(item)
            yield item
        for p in range(2,2001):
            url="https://search.51job.com/list/180200,000000,0000,00,9,99,%2520,2,"+str(p)+".html"
            yield scrapy.Request(url,callback=self.parse)