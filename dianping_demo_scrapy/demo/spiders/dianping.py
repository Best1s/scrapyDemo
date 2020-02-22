# -*- coding: utf-8 -*-
import scrapy
from ..items import  DemoItem


class DianpingSpider(scrapy.Spider):
    name = 'dianping'
    allowed_domains = ['dianping.com','www.dianping.com']
    search_words = ['美容院']
    start_urls = [f'http://www.dianping.com/search/keyword/4/0_{word}' for word in search_words ]
    
    def verify_url(self, status):
         self.crawler.engine.close_spider(self, 'url change, stop crawl!')

    def parse(self,response):
        '''
        按区爬取，获取全部区链接url  id="region-nav"
        '''
        #self.verify_url(url=response.url.split("/")[2])
        regions = response.xpath('//div[@id="region-nav"]/a')
        for region in regions:
            url = region.xpath('./@href').get()     
            yield scrapy.Request(url=url, callback=self.road_parse)

    def road_parse(self,response):
        '''
        按路爬取，获取每路的店铺列表url
        '''
        #self.verify_url(url=response.url.split("/")[2])

        roads = response.xpath('//div[@id="region-nav-sub"]/a')
        for road in roads:
            url = road.xpath('./@href').get()
            if url == response.url:
                continue
            yield scrapy.Request(url=url, callback=self.shop_list_parse)
        

    def shop_list_parse(self,response):
        '''
        爬取店铺url,获取下一页url
        '''
        #self.verify_url(url=response.url.split("/")[2])

        shop_urls = response.xpath('//div[@class="pic"]/a/@href').getall()  #店铺URL合集
        page = response.xpath('//div[@class="page"]/a[@class="cur"]/text()').get()     #当前页码数
        next_page_url =  response.xpath('//div[@class="page"]/a[last()]/@href').get()    #下一页url             

        print('正在爬取第',page,'页店铺')
        for url in shop_urls:
            print('正在爬取',url,'店铺信息')
            yield scrapy.Request(url=url, cookies = None, callback=self.shop_parse)
        
        if next_page_url:            
            yield scrapy.Request(url=next_page_url, callback=self.shop_list_parse)


    def shop_parse(self,response):
    #def parse(self,response):

        #self.verify_url(url=response.url.split("/")[2])

        title = response.xpath('//div[@id="basic-info"]/h1[@class="shop-name"]/text()').get()   #标题
        
        if title:
            title = title.strip()

        region = response.xpath('//div[@id="basic-info"]/div[@class="expand-info address"]/a/span/text()').get()
                             
        if region:
            address = "地址:" + region + response.xpath("//div[@class='expand-info address']/span/@title").get()   #格式：区加具体地址
        else:            
            address = None

        tel = response.xpath('//div[@id="basic-info"]/p[@class="expand-info tel"]/span[@itemprop="tel"]/text()').getall()   #电话
        url =  response.request.url     #店铺url

        print("*"*40 + "获取到数据" + '*'*40)

        item = DemoItem(title=title, tel=tel, address=address, url=url)
        yield item
                
