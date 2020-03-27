# -*- coding: utf-8 -*-
import scrapy
from ..items import  DemoItem


class DianpingSpider(scrapy.Spider):
    name = 'dianping'
    allowed_domains = ['dianping.com','www.dianping.com']
    classfiys = ['g158','g2572','g159']
    start_urls = [f"http://www.dianping.com/handan/ch50/{classfiy}" for classfiy in classfiys]

    def verify_url(self, status):
         self.crawler.engine.close_spider(self, 'url change, stop crawl!')

    def parse(self,response):
        '''
        按区爬取，获取全部区链接url  id="region-nav"
        '''
        #self.verify_url(url=response.url.split("/")[2])
        pages = response.xpath('//div[@class="page"]/a[last()-1]/@data-ga-page').get()  #获取页面数量如果小于50 直接爬取店铺url。
        if  pages and int(pages) < 50:
            yield scrapy.Request(url=response.url, callback=self.shop_list_parse,dont_filter=True)
        else:
            regions = response.xpath('//div[@id="region-nav"]/a')
            for region in regions:
                url = region.xpath('./@href').get()
                if url == "javascript:;":
                    continue
                yield scrapy.Request(url=url, callback=self.road_parse,dont_filter=True)

    def road_parse(self,response):
        '''
        区域内如果页面小于50直接解析店铺，未优化。
        按路爬取，获取每路的店铺列表url
        
        '''
        #self.verify_url(url=response.url.split("/")[2])

        roads = response.xpath('//div[@id="region-nav-sub"]/a')
        for road in roads:
            url = road.xpath('./@href').get()
            if url == response.url:
                continue
            yield scrapy.Request(url=url, callback=self.shop_list_parse,dont_filter=True)
        

    def shop_list_parse(self,response):
        '''
        爬取店铺url,获取下一页url
        '''
        #self.verify_url(url=response.url.split("/")[2])

        shop_urls = response.xpath('//div[@class="pic"]/a/@href').getall()  #店铺URL合集
        #page = response.xpath('//div[@class="page"]/a[@class="cur"]/text()').get()     #当前页码数
        next_page_url =  response.xpath('//div[@class="page"]/a[last()]/@href').get()    #下一页url             

        yield DemoItem(url=shop_urls)
        
        if next_page_url:            
            yield scrapy.Request(url=next_page_url, callback=self.shop_list_parse)


                
