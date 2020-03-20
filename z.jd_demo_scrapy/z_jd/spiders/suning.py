# -*- coding: utf-8 -*-
import scrapy
from z_jd.items import ZSnItem

class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['zc.suning.com']
    start_urls = [f'https://zc.suning.com/project/browseList.htm?c=&t=&s=&keyWords=&pageNumber={i}' for i in range(1,36)]
    #start_urls = ['https://zc.suning.com/project/browseList.htm?c=&t=&s=&keyWords=&pageNumber=1' ]



    def parse(self, response):
        urls = response.xpath("//div[@class='item-info']/p[@class='item-name']/a/@href").getall()
        for url in urls:
            url = "https://zc.suning.com" + url
            yield scrapy.Request(url=url, callback=self.page_parse)

    def page_parse(self, response):
        url = response.url        
        company_name = response.xpath("//div[@class='item-organizer box']/p[1]/text()").get()        
        try:
            tel = response.xpath("//div[@class='item-detail-right']/div[@class='item-organizer box']/p[@class='info'][2]/text()").get()
        except Exception as e:
            tel = 0
        print("******************************获取到数据*************************")
        print(company_name,tel,url)
        item = ZSnItem(company_name=company_name, tel=tel, url=url)
        yield item
