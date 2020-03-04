# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class DemoPipeline(object):
    def __init__(self):         #爬虫被打开时执行 同open_spider
        print('开始爬虫'*5)
        fileName = 'dianpingdata.csv'
        self.file = open(fileName, 'a+', newline='')
        self.file2 = open('dianpingshopurl.csv', 'a+', newline='')
        self.writer = csv.writer(self.file,dialect='excel')        
        self.writer2 = csv.writer(self.file2,dialect='excel')        

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):     #当item传值过来时会被调用。
        if not item["tel"] and item['url'].split("/")[2] == "verify.meituan.com":
            return item
        if not item['title'] and not item['address'] and not item['tel'] and item['url']:
            self.writer2.writerow([item['url'],item['title'],item['tel'],item['address']])
            return item
        self.writer.writerow([item['title'],item['tel'],item['address'],item['url']])
        return item

    def close_spider(self, spider):  #爬虫关闭时调用
        print('结束爬虫'*5)
        self.file.close()
