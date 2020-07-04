# -*- coding: utf-8 -*-
import scrapy

from shipin_11467_com_scrapy.items import Shipin11467ComScrapyItem


class A11467Spider(scrapy.Spider):
    name = '11467'
    allowed_domains = ['shipin.11467.com','expo.11467.com','11467.com','rizhao.11467.com']
    start_urls = ['http://shipin.11467.com/']    

    def parse(self, response):
        urls = response.xpath("//div[@class='box sidesubcat t5'][2]/div[@class='boxcontent']/dl[@class='homepcat'][2]/dd[*]/a/@href").getall()           #获取休闲食品链接
        print("home crawl urls:   ",urls)
        for url in urls:
            url = "http:" + url
            print("home url is :",url)
            yield scrapy.Request(url=url, callback=self.page_parse, dont_filter=True)

    def page_parse(self, response):
        next_page_url =  response.xpath('//div[@class="pages"]/a[last()-1]/@href').get()    #下一页url

        if next_page_url and next_page_url != response.xpath('//div[@class="pages"]/a[last()]/@href').get():
            yield scrapy.Request(url="http:" + next_page_url, callback=self.page_parse)
        urls = response.xpath("//div[@class='box'][1]/div[@class='imglist']/ul[@class='pli']/li[*]/dl/dt/a/@href").getall()     #解析页面店铺
        for url in urls:
            url = "http:" + url
            print("pages url is :",url)

            yield scrapy.Request(url=url, callback=self.shop_parse)       

    def shop_parse(self, response):

        
        title = response.xpath("//div[@class='producttitleintro']/h1[@class='product']/text()").get()
        dt = response.xpath("//div[@class='pdata']/dl[@id='pshowdata']/dt/text()").getall()
        #print("dt info is :", dt,"dt num is:",len(dt))
        #dds = response.xpath("//div[@class='pdata']/dl[@id='pshowdata']/dd")
        dtnum=len(dt)
        company_name = response.xpath(".//div[@class='pdata']/dl[@id='pshowdata']/dd[1]/strong/a/text()").get()
        
        name = response.xpath("//div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[" + str(dtnum) + "]/em/text()").get()
        if name :
            tel = response.xpath("//div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[" + str(dtnum - 1 ) + "]/strong/text()").get()
            if tel:
                phone = response.xpath("//div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[" + str(dtnum - 2 ) + "]/strong/text()").get()
                if phone:
                    address = response.xpath("//div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[" + str(dtnum - 3 ) + "]/text()").get()
                else:
                    phone = 0
                    address = response.xpath("//div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[" + str(dtnum - 2 ) + "]/text()").get()
        else:
            name = response.xpath("//div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[" + str(dtnum - 1) + "]/em/text()").get()
            tel = response.xpath("//div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[" + str(dtnum - 2 ) + "]/strong/text()").get()
            if tel:
                phone = response.xpath("//div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[" + str(dtnum - 3 ) + "]/strong/text()").get()
                if phone:
                    address = response.xpath("//div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[" + str(dtnum - 4 ) + "]/text()").get()
                else:
                    phone = 0
                    address = response.xpath("//div[1]/div[@class='pdata']/dl[@id='pshowdata']/dd[" + str(dtnum - 3 ) + "]/text()").get()
        

        url = response.url       

        print("******************************获取到数据*************************")
        print("shop  info s :", title, url, company_name, address, name ,tel, phone)
        item = Shipin11467ComScrapyItem(title=title, url=url, company_name=company_name, address=address, name=name,tel=tel, phone=phone)
        yield item

