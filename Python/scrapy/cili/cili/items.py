# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CiliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field ()
    formatSize = scrapy.Field ()
    date = scrapy.Field ()
    hot = scrapy.Field ()
    detailUrl = scrapy.Field ()
    magnet = scrapy.Field ()
