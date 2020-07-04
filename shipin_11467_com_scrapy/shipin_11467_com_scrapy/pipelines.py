# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class Shipin11467ComScrapyPipeline(object):

    def __init__(self):         #爬虫被打开时执行 同open_spider
        print('开始爬虫'*5)       
        fileName = '11467food.csv'
        self.file = open(fileName, 'a+', newline='')        
        self.writer = csv.writer(self.file,dialect='excel')                

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):     #当item传值过来时会被调用。
        # title=title, url=url, company_name=company_name, address=address, name=name,tel=tel, phone=phone
        
        self.writer.writerow([item['title'], item['name'], item['company_name'], item['tel'], item['phone'], item['address'], item['url']])
        return item
    def close_spider(self, spider):  #爬虫关闭时调用
        print('结束爬虫'*5)
        self.file.close()