# -*- coding: utf-8 -*-
import scrapy
from jd.items import JdItem


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']  # 有的时候写个www.jd.com会导致search.jd.com无法爬取
    keyword = "口红"
    page = 1
    url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8&wq=%s&page=%d&click=0'
    next_url = 'https://search.jd.com/s_new.php?keyword=%s&enc=utf-8&wq=%s&page=%d&scrolling=y&show_items=%s'


    def start_requests(self):
        yield scrapy.Request(self.url % (self.keyword, self.keyword, self.page), callback=self.parse)

    def parse(self, response):
        """
        爬取每页的前三十个商品，数据直接展示在原网页中
        :param response:
        :return:
        """
        ids = []
        x = 0
        for li in response.xpath('//*[@id="J_goodsList"]/ul/li'):
            x = x + 1
            item = JdItem()
            price = li.xpath('div/div/strong/i/text()').extract()  # 价格
            shop = li.xpath('div/div[@class="p-shop"]/span/a/text()').extract()  # 店铺
            tags = li.xpath('div/div[@class="p-icons"]/i/text()').extract()  # 标签
            title = li.xpath('div/div/a/em/text()').extract()  # 标题

            id = li.xpath('@data-pid').extract()  # id

            ids.append(''.join(id))

            url = li.xpath('div/div[@class="p-name p-name-type-2"]/a/@href').extract()  # 需要跟进的链接

            item['title'] = ''.join(title)
            item['keyword'] = ''.join(self.keyword)
            item['shop'] = ''.join(shop)
            item['price'] = ''.join(price)
            item['tags'] = ''.join(tags)
            item['url'] = ''.join(url)


            if item['url'].startswith('//'):
                item['url'] = 'https:' + item['url']
                yield item

        print('京东采集 ：' + self.keyword + '  显示页面已采集' + str(x) + '条，' + 'Page = ' + str(self.page))

        if x < 1:
            self.crawler.engine.close_spider(self, '已爬取所有信息！')
        else:

            headers = {'referer': response.url}
            # 后三十页的链接访问会检查referer，referer是就是本页的实际链接
            # referer错误会跳转到：https://www.jd.com/?se=deny
            self.page += 1
            yield scrapy.Request(self.next_url % (self.keyword, self.keyword, self.page, ','.join(ids)),
                                 callback=self.next_parse, headers=headers)

    def next_parse(self, response):
        """
        爬取每页的后三十个商品，数据展示在一个特殊链接中：url+id(这个id是前三十个商品的id)
        :param response:
        :return:
        """
        y = 0
        for li in response.xpath('//li[@class="gl-item"]'):
            y = y + 1
            item = JdItem()
            price = li.xpath('div/div/strong/i/text()').extract()  # 价格
            shop = li.xpath('div/div[@class="p-shop"]/span/a/text()').extract()  # 店铺
            tags = li.xpath('div/div[@class="p-icons"]/i/text()').extract()  # 标签
            title = li.xpath('div/div/a/em/text()').extract()  # 标题
            url = li.xpath('div/div[@class="p-name p-name-type-2"]/a/@href').extract()  # 需要跟进的链接

            item['title'] = ''.join(title)
            item['keyword'] = ''.join(self.keyword)
            item['shop'] = ''.join(shop)
            item['price'] = ''.join(price)
            item['tags'] = ''.join(tags)
            item['url'] = ''.join(url)

            if item['url'].startswith('//'):
                item['url'] = 'https:' + item['url']
                yield item

        print('京东采集 ：' + self.keyword + '  隐藏页面已采集' + str(y) + '条，' + 'Page = ' + str(self.page))
        if y < 1:
            self.crawler.engine.close_spider(self, '已爬取所有信息！')
        else:
        #if self.page < 200:
            self.page += 1
            yield scrapy.Request(self.url % (self.keyword, self.keyword, self.page), callback=self.parse)