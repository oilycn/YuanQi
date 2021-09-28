# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field ()
    money = scrapy.Field ()
    company = scrapy.Field ()
    company_url = scrapy.Field ()
    loc = scrapy.Field ()
    time = scrapy.Field ()
    url = scrapy.Field ()
