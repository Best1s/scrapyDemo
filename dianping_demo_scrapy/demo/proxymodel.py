import requests
import demo.uapool as ua
import random
import time
import signal
class Proxy(object):
    def __init__(self):
        self.url = "http://47.106.254.210/"
        self.headers = {'Authorization': 'Basic cHJveHk6cHJveHkxMjMh'}
        self.try_count = 0
        self.status = False
        #signal.signal(signal.SIGINT, self.signal_process)
    def delete_proxy(self,proxy):
        requests.get(self.url + "delete/?proxy={}".format(proxy), headers = self.headers)
        print("delete proxy ip success")

    def signal_process(self,signum, frame):
        print("this is ctrl + c！")
        self.status=True
        return exit
        
    def get_proxy(self,spider):
        def close_spider(spider):
            print("this is close_spider")
            spider.crawler.engine.close_spider(spider, '没有代理IP关闭爬虫')
        while True:
            try:
                ip = requests.get(self.url + "get/", headers = self.headers).json().get("proxy")
                if not ip :
                    #print("没有代理ip！可按Ctrl + c 中断")
                    #signal.signal(signal.SIGINT, close_spider)
                    time.sleep(5)
                r = requests.get("http://www.dianping.com",headers={"User-Agent":random.choice(ua.USER_AGENTS)}, proxies={"http":"http://" + ip}, timeout=3)
                time.sleep(0.5)
            #except requests.exceptions.ConnectionError :
            #    self.delete_proxy(proxy=ip)
            except Exception as e:
                self.delete_proxy(proxy=ip)
            else:                
                if r.status_code == 200:
                    break
                elif r.status_code == 500:
                    self.delete_proxy(proxy=ip)
        return "http://" + ip


