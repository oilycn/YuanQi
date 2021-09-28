# -*- coding: utf-8 -*-
import scrapy


class JdItem(scrapy.Item):

    title = scrapy.Field()  # 标题

    price = scrapy.Field()  # 价格

    shop = scrapy.Field()  # 价格

    tags = scrapy.Field()  # 标签

    url = scrapy.Field()  # 商品链接

    keyword = scrapy.Field()  # keyword
