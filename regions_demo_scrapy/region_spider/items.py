# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RegionSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    cname = scrapy.Field()
    pinyin_name = scrapy.Field()
    
