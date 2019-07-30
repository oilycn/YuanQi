# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from typing import Any

import scrapy
from scrapy import Field


class DouyuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    zhubo = scrapy.Field()
    url = scrapy.Field()
    fenlei = scrapy.Field()
    dengji = scrapy.Field()
    bankuai = scrapy.Field()
    biaoqian = scrapy.Field()
    vip = scrapy.Field()
    pass
