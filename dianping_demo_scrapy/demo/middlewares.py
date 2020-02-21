# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import time
import requests
import os
from selenium import webdriver

import demo.user_agent as ua

from scrapy.exceptions import IgnoreRequest
from twisted.internet.error import TimeoutError
from twisted.internet.defer import DeferredLock
from scrapy.http import HtmlResponse

class Proxy(object):
    def __init__(self):
        self.url = "http://47.106.254.210/"
        self.headers = {'Authorization': 'Basic cHJveHk6cHJveHkxMjMh'}
        self.lock = DeferredLock()
    def get_proxy(self):
        self.lock.acquire()
        ip = requests.get(self.url + "get/", headers = self.headers).json().get("proxy")
        try:
            r = requests.get("http://www.dianping.com",headers={"User-Agent":random.choice(ua.USER_AGENTS)}, proxies={"http":"http://" + ip}, timeout=3)
        except requests.exceptions.ConnectionError as Rerror:
            self.delete_proxy(proxy=ip)
            print(Rerror)
            self.get_proxy()
        except Exception as e:
            print(e)
            self.get_proxy()
        else:
            if r.status_code == 200:
                self.lock.release() 
                return ip
            else:
                self.get_proxy()
        

    def delete_proxy(self,proxy):
        requests.get(self.url + "delete/?proxy={}".format(proxy), headers = self.headers)

    # your spider code

    def getHtml(self):
        # ....
        retry_count = 5
        proxy = get_proxy().get("proxy")
        while retry_count > 0:
            try:
                html = requests.get('https://www.example.com', proxies={"http": "http://{}".format(proxy)})

                return html
            except Exception:
                retry_count -= 1

        delete_proxy(proxy)
        return None

class UseBrowser(object):
    def __init__(self, *args, **kwargs):
        self.lock = DeferredLock()
        driver_path = os.getcwd() + "\chromedriver80.0.3987.16.exe"
        self.browser = webdriver.Chrome(driver_path)
        self.browser.implicitly_wait(10)  # 隐性等待，最长等10秒
    
    def get_bro_cookies(self):
        self.lock.acquire()
        self.browser.get("http://www.dianping.com")
        cookies = self.browser.get_cookies()
        self.browser.quit()
        self.lock.release()

        return cookies

    def del_bro_cookies(self):
        self.lock.acquire()
        self.browser.delete_all_cookies()
        self.lock.release()
        return True

class DemoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DemoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.  
    def __init__(self):
        self.p = Proxy()
        self.browser = UseBrowser()
        self.current_proxy = None
   
          
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # - 当每个request通过下载中间件时，该方法被调用。，一般这里设置随机代理IP
        # - 如果其返回 None ，Scrapy将继续处理该request，执行其他的中间件的相应方法，直到合适的下载器处理函数(download handler)被调用， 该request被执行(其response被下载)。
        # - 如果其返回 Response 对象，Scrapy将不会调用 任何 其他的 process_request() 或 process_exception() 方法，或相应地下载函数； 
        #   其将返回该response。 已安装的中间件的 process_response() 方法则会在每个response返回时被调用。
        # - 如果其返回 Request 对象，Scrapy则停止调用 process_request方法并重新调度返回的request。当新返回的request被执行后， 相应地中间件链将会根据下载的response被调用。
        # - 如果其raise一个 IgnoreRequest 异常，则安装的下载中间件的 process_exception() 方法会被调用。
        #   如果没有任何一个方法处理该异常， 则request的errback(Request.errback)方法会被调用。如果没有代码处理抛出的异常， 则该异常被忽略且不记录(不同于其他异常那样)。
        

        request.headers["User-Agent"] = random.choice(ua.USER_AGENTS)        
            

        if not request.cookies:
            cookies = self.get_bro_cookies()
            print("*"*40)
            print("get cookies is",cookies)
            request.cookies = cookies
        if 'proxy' not in request.meta or self.current_proxy.is_expiring:
            # 请求代理
            self.p.get_proxy()
            request.meta['proxy'] = self.current_proxy.proxy

        return None


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        # - 如果其返回一个 Response ，会将新的response对象传给其它中间件，最终传给爬虫
        # - 如果其返回一个 Request 对象，则中间件链停止， 返回的request会被下载器调度下载。处理类似于 process_request() 返回request所做的那样。
        # - 如果其抛出一个 IgnoreRequest 异常，则调用request的errback(Request.errback)。 如果没有代码处理抛出的异常，则该异常被忽略且不记录(不同于其他异常那样)。  会抛出异常？还是不会？

        print("="*80)
        print("这是一个rsponse")
        if response.url.split("/")[2] == "verify.meituan.com":
            self.i = self.i+1
            self.browser.get(request.url)
            time.sleep(5)
            print("browser url is ",self.browser.current_url())
            request.url = self.browser.current_url()
            if self.i > 3: 
                self.i = 0
                return response
            else:
                return request
            #return response

        if response.status != 200 :
            self.i = self.i+1
            print("this is not 200 status ,cookies is ", request.cookies)
            print("url is:",request.url)
            #self.browser.add_cookie(request.cookies)
            self.browser.get(response.url)
            #request.cookies = None
            #self.browser.get(response.url)
            #response = HtmlResponse(url=self.browser.current_url,status=200,body=self.browser.page_source.encoding='utf-8',request=request)
            request.cookies=self.browser.get_cookies()
            print("renew url is",response.url)
            if self.i > 3: 
                self.i = 0
                return response
            else:
                return request
 
        
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        if isinstance(exception, TimeoutError):
            proxy_ip = request.meta["proxy"]
            print("TimeoutError,response proxy ip is :",proxy_ip)
            self.p.delete_proxy(proxy_ip)
            del request.meta["proxy"]
            return request
        #return request
        

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)





