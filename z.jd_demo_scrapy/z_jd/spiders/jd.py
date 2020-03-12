# -*- coding: utf-8 -*-
import scrapy
from z_jd.items import ZJdItem
from selenium import webdriver
import os
import time
from lxml import etree
import csv


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']

    def __init__(self):
        self.file = open('123.csv', 'r', newline='')
        self.f_csv = csv.reader(self.file)
    #    self.driver_path = os.getcwd() + "\chromedriver80.0.3987.16.exe"
    #    self.browser = webdriver.Chrome(self.driver_path)
    #    self.browser.implicitly_wait(10)  # 隐性等待，最长等10秒
    #    self.browser.set_window_size(700, 1000)
    #    self.root_url = "https://z.jd.com/bigger/search.html" 

    def start_requests(self):      
        #self.browser.get(self.root_url)
        #time.sleep(3)
        #for i in range(2,10):
        #    self.browser.find_element_by_xpath("//ul[@class='l-list clearfix fl']/li[@class='fl'][2]/a[@id='parentId']").click()
        #    time.sleep(3)        
        #    while True:
        #        html = etree.HTML(self.browser.page_source)
        #        zc_urls = html.xpath("//div[@class='i-tits  no-color-choose']/a/@href")       
        #        for url in zc_urls:
        #            print(url)
        #            yield scrapy.Request(url="http://z.jd.com" + url, callback=self.parse)
        #        if html.xpath("//div[@class='pagesbox']/div[@id='page_div']/a[@class='next']/text()"):
        #            try:
        #                self.browser.find_element_by_xpath("//div[@class='pagesbox']/div[@id='page_div']/a[@class='next']").click()
        #                time.sleep(2)
        #            except Exception as e:
        #                print(e)
        #        else:
        #            break
        for url in self.f_csv:
            #yield scrapy.Request(url="http://z.jd.com" + url[0], callback=self.parse)
            yield scrapy.Request(url=url[0], callback=self.parse)



    def parse(self, response):
        url = response.url
        company_name = response.xpath("//li[@class='clearfix contact-li'][1]/div[@class='val']/text()").get()
        try:
            address = response.xpath("//li[@class='clearfix contact-li'][2]/div[@class='val']/text()").get().split()
        except Exception as e:
            address = None
        tel = response.xpath("//li[@class='clearfix contact-li'][3]/div[@class='val']/text()").get()
        print("******************************获取到数据*************************")
        item = ZJdItem(company_name=company_name, address=address, tel=tel, url=url)
        yield item
