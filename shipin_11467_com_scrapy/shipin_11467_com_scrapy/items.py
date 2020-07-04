# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Shipin11467ComScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # title=title, url=url, company_name=company_name, address=address, name=name,tel=tel, phone=phone
    title = scrapy.Field()
    url = scrapy.Field()
    company_name = scrapy.Field()
    address = scrapy.Field()
    name = scrapy.Field()
    tel = scrapy.Field()
    phone = scrapy.Field()
