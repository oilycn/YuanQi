import scrapy
from douyu.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = "douyu"
    allowed_domains = ['douyu.com']
    start_urls = [
        'https://www.douyu.com/directory/all'
    ]

    def parse(self, response):
        urls = response.xpath('//a[@class="Aside-menu-item"]/@href').extract()
        for url in urls:
            urljin = 'https://www.douyu.com' + url
            yield response.follow(urljin, callback=self.parse_nexts)


    def parse_nexts(self,response):
        #print(response.url)
        datas = response.xpath('//ul[@class="layout-Cover-list"]//a[@class="DyListCover-wrap"]/@href').extract()
        for data in datas:
            jin_url = 'https://www.douyu.com' + data
            yield scrapy.Request(jin_url,callback=self.parse_details)

    def parse_details(self,response):
        print(response.url)
        title = response.xpath('//h3[@class="Title-headlineH2"]/text()').extract_first()
        zhubo = response.xpath('//a[@class="Title-anchorName"]/@title').extract_first()
        url = response.url
        dengji = response.xpath('//div[@class="Title-AnchorLevel"]/div/@class').re(r'\d+\.?\d*')[0]
        bankuai = response.xpath('//div[@class="Title-categoryList clearFix"]/a[1]/text()').extract_first()
        fenlei = response.xpath('//div[@class="Title-categoryList clearFix"]/a[2]/text()').extract_first()
        biaoqian = response.xpath('//div[@class="Title-categoryList clearFix"]/a[3]/text()').extract_first()

        #renqi = response.xpath('//div[@id="live-list-content"]//span[@class="dy-num fr"]/text()').extract_first()

        item = DouyuItem()
        item['title'] = title
        item['zhubo'] = zhubo
        item['url'] = url
        item['fenlei'] = fenlei
        item['dengji'] = dengji
        item['bankuai'] = bankuai
        item['biaoqian'] = biaoqian
        # print(renqi)
        yield item



