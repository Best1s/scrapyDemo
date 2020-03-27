# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from redis import StrictRedis, ConnectionPool
import demo.settings as settings
import MySQLdb


class DemoPipeline(object):
    def __init__(self):         #爬虫被打开时执行 同open_spider
        print('开始爬虫'*5)
        host = settings.REDIS_HOST
        port = settings.REDIS_PORT
        password = settings.REDIS_PASSWORD
        self.pool = ConnectionPool(host=host, port=port,  password=password)
        self.redis = StrictRedis(connection_pool=self.pool)        
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):     #当item传值过来时会被调用。
        for url in item['url']:
            if not self.redis.sismember("set_shop_url",url) and not self.redis.sismember("lpushed_shop_url",url):                
                self.redis.lpush("dianping:start_urls",url)
                self.redis.sadd("lpushed_shop_url",url)
            else:
                continue
        print("url添加成功")
        return item

    def close_spider(self, spider):  #爬虫关闭时调用
        print('结束爬虫'*5)
        print("剩余商店爬虫数据：",self.redis.llen("dianping:start_urls"))
        print("总共爬取商店数据：",self.redis.scard("set_shop_url"))
        print("lpush数据：",self.redis.scard("lpushed_shop_url"))

class ShopPipeline(object):
    def __init__(self):         #爬虫被打开时执行 同open_spider
        print('开始爬虫'*5)
        self.host = settings.DB_HOST
        self.user = settings.DB_USER
        self.password = settings.DB_PASSWORD
        self.database = settings.DB_DATABASE

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):     #当item传值过来时会被调用。
        self.db = MySQLdb.connect(self.host, self.database, self.password, self.user, charset='utf8')
        self.cursor = self.db.cursor()
        if not item["tel"] and item['url'].split("/")[2] == "verify.meituan.com":
            return item
        if item["tel"]:
            tel = ",".join(item["tel"])
        else:
            tel = 0
        sql = "INSERT INTO shop_info (title, tel, address, shop_url) \
               VALUES ('%s', '%s', '%s', '%s')" % (item['title'], tel, item['address'], item['url'])
        try:
             # 执行sql语句             
             self.cursor.execute(sql)
             # 提交到数据库执行
             self.db.commit()
        except:
             # Rollback in case there is any error
             print("sql No insert !")
             self.db.rollback()
        self.db.close()
        return item
        
    def close_spider(self, spider):  #爬虫关闭时调用
        print('结束爬虫'*5)

        
