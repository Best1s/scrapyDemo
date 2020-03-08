# -*- coding: utf-8 -*-
import scrapy
from z_jd.items import ZJdItem
from selenium import webdriver
import os
import time


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
        classfiy_nums = self.browser.find_element_by_xpath("//ul[@class='l-list clearfix fl']/li[@class='fl'][*]/a[@id='parentId']") #not get()
        for i in range(2,len(classfiy_nums)+1):
            self.browser.find_element_by_xpath(f"//ul[@class='l-list clearfix fl']/li[@class='fl'][{i}]/a[@id='parentId']").click()
            time.sleep(3)




        #for zc_classfiy in zc_classfiys:
        #    zc_classfiy.click()
        #    time.sleep(5)
            #zc_urls = self.browser.find_element_by_xpath("//div[@class='l-result']/ul[@class='infos clearfix']/li[@class='info type_now']/a/@href").get()
            #for url in zc_urls:
            #    yield scrapy.Request(url="http://z.jd.com/" + url, callback=self.parse)

    def parse(self, response):
        pass
