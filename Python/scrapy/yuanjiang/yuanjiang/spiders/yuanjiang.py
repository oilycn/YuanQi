import scrapy
from yuanjiang.items import YuanjiangItem


class YuanjiangSpider( scrapy.Spider ):
    name = "oxmo"
    # allowed_domains = ['company.d17.cc']
    url = 'https://company.d17.cc/list/0_0_'
    page = 1
    start_urls = [url + str(page) + '.htm']

    # def start_requests(self):
    #     yield scrapy.Request(self.url % (self.page), callback=self.parse)

    def parse ( self, response ):
        jins = response.xpath( '//div[@class="companylist_style"]/ul/li' )
        for jin in jins:
            item = YuanjiangItem ()
            item['gs'] = jin.xpath ('*//div[@class="name clr"]/a/text()').extract_first()
            item['url'] = jin.xpath ('*//div[@class="name clr"]/a[1]/@href').extract_first()
            item['info'] = jin.xpath ('*//div[@class="info"]/span[3]/text()').extract_first()
            item['pmain'] = jin.xpath ('*//div[@class="pmain"]/text()').extract_first()
            item['cp_url'] = jin.xpath ('./div[@class="companylist_style_right"]/a[2]/@href').extract_first()
            lx_url = jin.xpath ('./div[@class="companylist_style_right"]/a[3]/@href').extract_first()
            item['lx_url'] = lx_url
            yield scrapy.Request (lx_url,meta={'key':item}, callback=self.parse_details)

    def parse_details(self,response):
        item = response.meta['key']
        people = response.xpath('//div[@class="pagein_contact clr"]/ul[@class="clr"]/li[1]/text()').extract_first()
        phone = response.xpath('//div[@class="pagein_contact clr"]/ul[@class="clr"]/li[2]/em/text()').extract_first()
        item['people'] = people
        item ['phone'] = phone
        print (item)
        yield item

        if self.page < 10:
            self.page += 1
            yield scrapy.Request (self.url + str(self.page) + '.htm', callback=self.parse)