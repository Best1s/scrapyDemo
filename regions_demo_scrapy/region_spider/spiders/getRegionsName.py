# -*- coding: utf-8 -*-
import scrapy

from region_spider.items import RegionSpiderItem


class GetregionsnameSpider(scrapy.Spider):
    name = 'getRegionsName'
    allowed_domains = ['baike.baidu.com']
    #23个省 
    province = ["https://baike.baidu.com/item/%E6%B2%B3%E5%8C%97%E7%9C%81/153775",
                    "https://baike.baidu.com/item/%E5%B1%B1%E8%A5%BF%E7%9C%81/365266",
                    "https://baike.baidu.com/item/%E8%BE%BD%E5%AE%81%E7%9C%81/739981",
                    "https://baike.baidu.com/item/%E5%90%89%E6%9E%97%E7%9C%81/129609",
                    "https://baike.baidu.com/item/%E9%BB%91%E9%BE%99%E6%B1%9F%E7%9C%81/129397",
                    "https://baike.baidu.com/item/%E6%B1%9F%E8%8B%8F%E7%9C%81/320938",
                    "https://baike.baidu.com/item/%E6%B5%99%E6%B1%9F%E7%9C%81/190275",
                    "https://baike.baidu.com/item/%E5%AE%89%E5%BE%BD%E7%9C%81/526353",
                    "https://baike.baidu.com/item/%E7%A6%8F%E5%BB%BA%E7%9C%81/122534",
                    "https://baike.baidu.com/item/%E6%B1%9F%E8%A5%BF/215383",
                    "https://baike.baidu.com/item/%E5%B1%B1%E4%B8%9C%E7%9C%81/209822",
                    "https://baike.baidu.com/item/%E6%B2%B3%E5%8D%97%E7%9C%81/59474",
                    "https://baike.baidu.com/item/%E6%B9%96%E5%8C%97%E7%9C%81/210064",
                    "https://baike.baidu.com/item/%E6%B9%96%E5%8D%97%E7%9C%81/293174",
                    "https://baike.baidu.com/item/%E5%B9%BF%E4%B8%9C%E7%9C%81/132473",
                    "https://baike.baidu.com/item/%E6%B5%B7%E5%8D%97%E7%9C%81/533000",
                    "https://baike.baidu.com/item/%E5%9B%9B%E5%B7%9D%E7%9C%81/15626925",
                    "https://baike.baidu.com/item/%E8%B4%B5%E5%B7%9E/37015",
                    "https://baike.baidu.com/item/%E4%BA%91%E5%8D%97",
                    "https://baike.baidu.com/item/%E9%99%95%E8%A5%BF",
                    "https://baike.baidu.com/item/%E7%94%98%E8%82%83%E7%9C%81/684374",
                    "https://baike.baidu.com/item/%E9%9D%92%E6%B5%B7/31638",
                    "https://baike.baidu.com/item/%E5%8F%B0%E6%B9%BE/122340"]
    #5个自治区
    zizhiqu = ["https://baike.baidu.com/item/%E5%86%85%E8%92%99%E5%8F%A4/173741",
                "https://baike.baidu.com/item/%E5%B9%BF%E8%A5%BF%E5%A3%AE%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8C%BA",
                "https://baike.baidu.com/item/%E8%A5%BF%E8%97%8F%E8%87%AA%E6%B2%BB%E5%8C%BA",
                "https://baike.baidu.com/item/%E5%AE%81%E5%A4%8F%E5%9B%9E%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8C%BA/11229891",
                "https://baike.baidu.com/item/%E6%96%B0%E7%96%86%E7%BB%B4%E5%90%BE%E5%B0%94%E8%87%AA%E6%B2%BB%E5%8C%BA"]
    start_urls = province + zizhiqu
    start_urls = ['https://baike.baidu.com/item/%E6%B2%B3%E5%8C%97%E7%9C%81/153775']
    #4个直辖市
    zhixiashi = {"北京":"beijing","天津":"tainjin","上海":"shanghai","重庆":"chongqing"}
    #2个特别区
    tebiequ = {"香港":"xianggamg","台湾":"taiwan"}
    def __init__(self):
        self.root_url = "https://baike.baidu.com"

    def parse(self, response):
        regions = response.xpath("//table[@class='table-view log-set-param'][1]/tbody/tr/td[1]//a")
        for region_url in regions:
            url = regions.xpath('./@href').get()
            if url:
                yield scrapy.Request(url=self.root_url + url, callback=self.region_parse)

    def region_parse(self, response):
        cname = response.xpath("//div[@class='basic-info cmn-clearfix']/dl[@class='basicInfo-block basicInfo-left']/dd[@class='basicInfo-item value'][1]/text()").get()
        if cname:
            cname = cname.strip()
        pinyin_name = response.xpath("//dl[@class='basicInfo-block basicInfo-left']/dd[@class='basicInfo-item value'][2]/text()").get()
        if pinyin_name:
            pinyin_name = pinyin_name.strip()

        print(cname,pinyin_name)
        item = RegionSpiderItem(cname=cname,pinyin_name=pinyin_name)
        yield item
        

        
