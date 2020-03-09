# -*- coding: utf-8 -*-
import scrapy
from z_jd.items import ZJdItem
from selenium import webdriver
import os
import time
from lxml import etree


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']

    def __init__(self):
        self.driver_path = os.getcwd() + "\chromedriver80.0.3987.16.exe"
        self.browser = webdriver.Chrome(self.driver_path)
        self.browser.implicitly_wait(10)  # 隐性等待，最长等10秒
        self.browser.set_window_size(700, 1000)

    def start_requests(self):
        root_url = "https://z.jd.com/bigger/search.html"        
        self.browser.get(root_url)
        time.sleep(3)
        zc_urls = []
        for i in range(2,10):
            try:
                self.browser.find_element_by_xpath(f"//ul[@class='l-list clearfix fl']/li[@class='fl'][{i}]/a[@id='parentId']").click()
                time.sleep(3)
            except(e):
                print(e)            
            while True:
                html = etree.HTML(self.browser.page_source)
                print("next url is :")
                print(html.xpath("//div[@class='pagesbox']/div[@id='page_div']/a[@class='next']/text()"))
                zc_urls = zc_urls + html.xpath("//div[@class='l-result']/ul[@class='infos clearfix']/li[@class='info type_now']/a/@href")
                if html.xpath("//div[@class='pagesbox']/div[@id='page_div']/a[@class='next']/text()"):
                    self.browser.find_element_by_xpath("//div[@class='pagesbox']/div[@id='page_div']/a[@class='next']").click()
                    time.sleep(3)
                else:
                    break
        for url in zc_urls:
            yield scrapy.Request(url="http://z.jd.com" + url, callback=self.parse)

    def parse(self, response):
        url = response.url
        company_name = response.xpath("//li[@class='clearfix contact-li'][1]/div[@class='val']/text()").get()
        address = response.xpath("//li[@class='clearfix contact-li'][2]/div[@class='val']/text()").get().split()
        tel = response.xpath("//li[@class='clearfix contact-li'][3]/div[@class='val']/text()").get()
        print("******************************获取到数据*************************")
        item = ZJdItem(company_name=company_name, address=address, tel=tel, url=url)
        yield item
