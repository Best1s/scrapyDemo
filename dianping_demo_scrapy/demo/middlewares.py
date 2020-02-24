# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from twisted.internet.error import TimeoutError
from selenium.common.exceptions import TimeoutException
#from twisted.internet.defer import DeferredLock
#from scrapy.http import HtmlResponse



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


        
        #try:            
        #    if request.url.split("/")[2] == "verify.meituan.com":
        #        self.proxy_status = False
        #        self.lock.acquire()
        #        self.browser.delete_all_cookies()
        #        time.sleep(3)
        #        self.browser.get("http://www.dianping.com")
        #        self.browser.get(request.url,proxies={"http":self.p.get_proxy()})
        #        self.lock.release()
        #    else:
        #        self.browser.get(request.url)
        #except TimeoutException:
        #    return HtmlResponse(url=request.url, status=500, request=request)
        #else:
        #    return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8', status=200)
        #response.url.split("/")[2] == "verify.meituan.com":

        #if response.status != 200 :
        #    request.cookies = None
        #    request.meta["proxy"] = self.p.get_proxy()
        #    return request
            #response = HtmlResponse(url=self.browser.current_url,status=200,body=self.browser.page_source.encoding='utf-8',request=request)        
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        if isinstance(exception, TimeoutError):
            pass
        return None
        

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)





