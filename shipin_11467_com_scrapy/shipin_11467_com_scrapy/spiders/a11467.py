# -*- coding: utf-8 -*-
import scrapy

from shipin_11467_com_scrapy.items import Shipin11467ComScrapyItem


class A11467Spider(scrapy.Spider):
    name = '11467'
    allowed_domains = ['shipin.11467.com']
    start_urls = ['http://shipin.11467.com/']    

    def parse(self, response):
        #urls = response.xpath("//div[@class='box sidesubcat t5'][2]/div[@class='boxcontent']/dl[@class='homepcat'][2]/dd[*]/a/@href").getall()           #获取休闲食品链接
        urls = response.xpath("//div[@class='box sidesubcat t5'][2]/div[@class='boxcontent']/dl[@class='homepcat'][2]/dd[1]/a/@href").getall()           #获取休闲食品链接
        print("xxxxxxxxxxxxxxxxxxxxx:   ",urls)
        for url in urls:
            url = "http:" + url
            print("home url is :",url)
            yield scrapy.Request(url=url, callback=self.page_parse)
    def page_parse(self, response):

        #urls = response.xpath("//div[@class='box'][1]/div[@class='imglist']/ul[@class='pli']/li[*]/dl/dt/a/@href").getall()     #解析页面店铺
        print("xxxxxxxxxxxxxxxxxxx",response.url)
        urls = response.xpath("//div[@class='box'][1]/div[@class='imglist']/ul[@class='pli']/li[*]/dl/dt/a/@href").getall()
        print("2222222222222222222222222",urls)
        for url in urls:
            url = "http:" + url
            print("2222222222222222222222pages url is :",url)
            #yield scrapy.Request(url=url, callback=self.shop_parse)       

    def shop_parse(self, response):
        url = response.url        
        company_name = response.xpath("//div[@class='  pcontent t10 pinfotop']/div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[1]/strong/a/text()").get()
        address = response.xpath("//div[@class='  pcontent t10 pinfotop']/div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[4]/text()").get()
        name = response.xpath("//div[@class='  pcontent t10 pinfotop']/div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[7]/em").get()         
        try:
            tel = response.xpath("//div[@class='  pcontent t10 pinfotop']/div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[5]/strong/text()").get()
            phone = response.xpath("//div[@class='  pcontent t10 pinfotop']/div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[6]/strong/text()").get()
        
        except Exception as e:
            tel = 0
            phone = 0
        print("******************************获取到数据*************************")
        print("shop  info s :",url , company_name, address, name ,tel, phone)
        #item = Shipin11467ComScrapyItem(company_name=company_name, tel=tel, url=url)
        #yield item

