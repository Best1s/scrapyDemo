# -*- coding: utf-8 -*-
import scrapy
from ..items import  ShopItem
from redis import StrictRedis, ConnectionPool
import time
from scrapy_redis.spiders import RedisSpider

class ShopParseSpider(RedisSpider):
    name = 'shop_parse'
    allowd_domains = ["www.dianping.com"]
    redis_key = 'dianping:start_urls'



    def parse(self, response):
        title = response.xpath('//div[@id="basic-info"]/h1[@class="shop-name"]/text()').get()   #标题
        
        if title:
            title = title.strip()

        region = response.xpath('//div[@id="basic-info"]/div[@class="expand-info address"]/a/span/text()').get()
                             
        if region:
            try:
                address = "地址:" + region + response.xpath("//div[@class='expand-info address']/span/@title").get()   #格式：区加具体地址
            except Exception:
                address = None
        else:            
            address = None

        tel = response.xpath('//div[@id="basic-info"]/p[@class="expand-info tel"]/span[@itemprop="tel"]/text()').getall()   #电话
        url =  response.request.url     #店铺url

        print("*"*40 + "获取到数据" + '*'*29)

        item = ShopItem(title=title, tel=tel, address=address, url=url)
        yield item
