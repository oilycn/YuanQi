# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YuanjiangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    gs= scrapy.Field()
    url = scrapy.Field()
    info = scrapy.Field()
    pmain = scrapy.Field()
    cp_url = scrapy.Field()
    lx_url = scrapy.Field()
    people = scrapy.Field()
    phone = scrapy.Field()

