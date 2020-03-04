from selenium import webdriver
import os
import time
import random
from scrapy.http import HtmlResponse
from twisted.internet.defer import DeferredLock

class UseBrowser(object):
    #功能：使用selenium渲染页面获取cookies，重新构造response返回给scrapy

    def __init__(self):
        self.driver_path = os.getcwd() + "\chromedriver80.0.3987.16.exe"
        self.browser = webdriver.Chrome(self.driver_path)
        self.browser.implicitly_wait(10)  # 隐性等待，最长等10秒
        self.browser.set_window_size(700, 1000)
        self.browser.get("http://www.dianping.com")
    
    def get_bro_cookies(self,url):
        self.browser.get("http://www.dianping.com/baoding")
        time.sleep(2)        
        while True:
            now_handle = self.browser.current_window_handle
            self.browser.get(url)            
            all_handles = self.browser.window_handles
            for handle in all_handles: 
                if handle != now_handle:   # 获取到与当前窗口不一样的窗口
                    self.browser.switch_to.window(handle)   # 切换
            if not self.browser.get_cookies():
                self.browser.delete_all_cookies()
                self.browser.get("http://www.dianping.com")
                self.browser.get(url)
            else:
                break        
        cookies = self.browser.get_cookies()
        c = {}
        for cookie in cookies:
            #if cookie["name"] == "_lxsdk_s":
            #    cookie["value"] = self.dispose_lxsdk_s(cookie["value"])
            c[cookie["name"]] = cookie["value"]
        #cookies = "cy=4; cityid=4; cye=guangzhou; cy=4; cye=guangzhou; _lxsdk_cuid=1706866c128c8-08ea7fb354e66e-313f68-1fa400-1706866c128c8; _lxsdk=1706866c128c8-08ea7fb354e66e-313f68-1fa400-1706866c128c8; _hc.v=51eb7fb0-09e5-bb42-a65e-2c68b953553e.1582299530; s_ViewType=10; _lxsdk_s=1706866b3f3-8cc-9f0-38e%7C%7C68"
        #cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}
        self.browser.delete_all_cookies()
        
        #self.browser.close()
        return c

    def dispose_lxsdk_s(self,cookie):
        cookie = cookie.split("%7C%7C")
        new_value =  cookie[0] + "%7C%7C" + str(int(cookie[1])+2)
        return new_value

    def get_response(self,request):
        try:
            self.browser.get(request.url)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)
        else:
            body = self.browser.page_source
            c = {}
            for cookie in self.browser.get_cookies():                
                c[cookie["name"]] = cookie["value"]
            self.browser.delete_all_cookies()
            #request.cookies = c
            self.browser.close()
            return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request, status=200)
    def get_request(self):
        pass

class CookiesDownloaderMiddleware(object):
    def __init__(self):
        self.browser = UseBrowser()
        self.cookies_status = False
        self.lock = DeferredLock()

    def process_request(self, request, spider):

        print("this is request in cookies middleware!!!")
        if request.url == "http://www.dianping.com/baoding/ch50/g123":
            self.lock.acquire()
            print("第一次爬取，从浏览器的root_url获取response")

            response = self.browser.get_response(request)
            print("*"*40)
            print(response.request.cookies)
            self.lock.release()
            return response

        if not request.cookies :
            print("request.url is ",request.url)
            self.lock.acquire()
            cookies = self.browser.get_bro_cookies(request.url)            
            request.cookies = cookies
            self.lock.release()
        print("request.cookies is ",request.cookies)
        print("request.ua is ",request.headers["User-Agent"])
        return None

    def process_reponse(self, request, response, spider):
        print("this is response in cookies middleware!!!")
        try_count = 3
        if response.url.split("/")[2] == "verify.meituan.com" or response.status == 403:
            self.lock.acquire()
            request.cookies = None
            self.lock.release()
            try_count -= 1
            return request
        elif try_count == 0 :
            try_count = 3
            return response
        return response






