import scrapy
from oxmo.items import OxmoItem


class OxmoSpider( scrapy.Spider ):
    name = "oxmo"
    allowed_domains = ['company.d17.cc']
    url = 'https://company.d17.cc/list/0_0_%d.htm'
    page = 1

    def start_requests(self):
        yield scrapy.Request(self.url % (self.page), callback=self.parse)

    def parse ( self, response ):
        # print(response.url)
        datas = response.xpath( '//div[@class="companylist_style"]/ul/li[@class="clr"]' )
        for jin in datas:
            gs = jin.xpath('//div[@class="name clr"]/a/text()').extract_first()
            url = jin.xpath('//div[@class="name clr"]/a/@href').extract_first()
            info = jin.xpath('//div[@class="info"]/span/text()').extract_first()
            pmain = jin.xpath('//div[@class="pmain"]/text()').extract_first()
            cp_url = jin.xpath('//div[@class="companylist_style_right"]/a[@title="公司产品"]/@href').extract_first()
            lx_url = jin.xpath('//div[@class="companylist_style_right"]/a[@title="联系方式"]/@href').extract_first()
            item = OxmoItem()
            item['gs'] = gs
            item['url'] = url
            item['info'] = info
            item['pmain'] = pmain
            item['cp_url'] = cp_url
            item['lx_url'] = lx_url
            print(item)
            if self.page < 20:
                self.page = self.page + 1
                yield scrapy.Request(self.url % (self.page), meta={'item': item}, callback=self.parse)
            # lxs_url = datas.xpath('//div[@class="companylist_style_right"]')
            # for lxfs in lxs_url:
            #     q_url = lxfs.xpath('//a[@title="联系方式"]/@href').extract_first()
            #     yield scrapy.Request( q_url, callback=self.parse_detail ,meta={'item':item})

        # def parse_detail ( self, response ):
        #     print(response.url)
        #     contact = response.xpath('//div[@class="pagein_contact clr"]/ul/li/text()').extract_first()
        #     item = OxmoItem( )
        #     item['contact'] = contact
        #     print(item)
        #     if self.page < 100:
        #         self.page = self.page + 1
        #         yield scrapy.Request(self.url % (self.page), meta={'item': item}, callback=self.parse)
