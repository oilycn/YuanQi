# -*- coding: utf-8 -*-
import scrapy
from boss.items import BossItem
import re
class ZpSpider(scrapy.Spider):
    name = 'zp'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=&city=101200100&industry=&position=']

    def parse(self, response):
        datas=response.xpath('//div[@class="job-list"]/ul/li').extract()
        item=BossItem()
        for i in range(0,len(datas)):
            data=datas[i]
            item["title"] = re.findall ('<div class="job-title">(.*?)</div>',  data,re.S)[0]
            item["money"] = re.findall ('<span class="red">(.*?)</span>', data, re.S)[0]
            item["loc"] = re.findall ('<p>(.*?)<em class="vline">', data, re.S)[0]
            url = re.findall ('<a href="(/job_detail/.*?)"', data, re.S)[0]
            item["url"] = "https://www.zhipin.com" + url
            item["sb_time"] = re.findall ('em class="vline"></em>(.*?)<em', data, re.S)[0]
            item["school"] = re.findall ('<em class="vline"></em>.*?<em class="vline"></em>(.*?)</p>', data, re.S)[0]
            item["company"] = re.findall ('<h3 class="name"><.*?>(.*?)</a></h3>', data, re.S)[0]
            item["company_rs"] = re.findall ('<em class="vline"></em>.*?<em class="vline"></em>(.*?)</p>', data, re.S)[1]
            # print(item)
            yield item
        next_page=response.xpath('//a[@ka="page-next"]/@href').extract()[0]
        if len(next_page)!=0:
            next_url="https://www.zhipin.com"+next_page
            yield scrapy.Request(next_url,callback=self.parse)