# -*- coding: utf-8 -*-
import scrapy
from ..items import  ShopItem
import datetime
from scrapy_redis.spiders import RedisSpider
from redis import StrictRedis, ConnectionPool
import demo.settings as settings
class ShopParseSpider(RedisSpider):
    name = 'shop_parse'
    redis_key = 'dianping:start_urls'
    #定义这个Spider所特有的Settings
    
    to_day = datetime.datetime.now()
    log_file_path = 'log/scrapy_{}_{}_{}.log'.format(to_day.year, to_day.month, to_day.day)
    
    custom_settings = {
        'ITEM_PIPELINES' : {
        'demo.pipelines.ShopPipeline': 320,
        # Store scraped item in redis for post-processing. 分布式redispipeline
        'scrapy_redis.pipelines.RedisPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES' : {
        'demo.uamiddleware.UaDownloaderMiddleware': 544,
        #'demo.proxymiddleware.ProxyMiddleWare': 570,
        'demo.slaveproxymiddleware2.ProxyMiddleWare': 570,
        },
        'COOKIES_ENABLED' : True,
        'JOBDIR' : 'slave_jobs_dir',
        'LOG_LEVEL' : 'DEBUG',
        'CONCURRENT_REQUESTS' : 50,
        #'LOG_FILE' : log_file_path,
    }

    def __init__(self, *args, **kwargs):
        host = settings.REDIS_HOST
        port = settings.REDIS_PORT
        password = settings.REDIS_PASSWORD
        self.pool = ConnectionPool(host=host, port=port,  password=password)
        self.redis = StrictRedis(connection_pool=self.pool)
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
        if response.status in [200]:
            self.redis.sadd("set_shop_url",url)
            yield item
        else:
            pass
