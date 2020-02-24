from selenium import webdriver
import os
import time
import random
from demo.capool import COOKIES as capool
class UseBrowser(object):
    def __init__(self):
        self.driver_path = os.getcwd() + "\chromedriver80.0.3987.16.exe"
        self.browser = webdriver.Chrome(self.driver_path)
        self.browser.implicitly_wait(10)  # 隐性等待，最长等10秒
        self.browser.set_window_size(700, 1000)
        self.browser.get("http://www.dianping.com")
    
    def get_bro_cookies(self,url):

        self.browser.get(url)
        cookies = self.browser.get_cookies()
        c = {}
        for cookie in cookies:
            if cookie["name"] == "_lxsdk_s":
                cookie["value"] = self.dispose_lxsdk_s(cookie["value"])
            c[cookie["name"]] = cookie["value"]
        #cookies = "cy=4; cityid=4; cye=guangzhou; cy=4; cye=guangzhou; _lxsdk_cuid=1706866c128c8-08ea7fb354e66e-313f68-1fa400-1706866c128c8; _lxsdk=1706866c128c8-08ea7fb354e66e-313f68-1fa400-1706866c128c8; _hc.v=51eb7fb0-09e5-bb42-a65e-2c68b953553e.1582299530; s_ViewType=10; _lxsdk_s=1706866b3f3-8cc-9f0-38e%7C%7C68"
        #cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}
        self.browser.delete_all_cookies()
        self.browser.close()
        return c

    def dispose_lxsdk_s(self,cookie):
        cookie = cookie.split("%7C%7C")
        new_value =  cookie[0] + "%7C%7C" + str(int(cookie[1])+2)
        return new_value

class CookiesPool(object):

    def get_cookies(self):
        cookies = random.choice(capool)
        cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}
        return cookies

class CookiesDownloaderMiddleware(object):
    def __init__(self):
        self.browser = UseBrowser()
        self.cookies_status = False

    def process_request(self, request, spider):
        print("this is cookies middleware!!!")
        if not request.cookies :
            cookies = self.browser.get_bro_cookies(request.url)
            print("获取到cookies：", cookies)
            request.cookies == cookies            
        return None


class CookiesDownloaderMiddleware2(object):
    def __init__(self):
        self.ca = CookiesPool()
        self.cookies_status = False
    def process_request(self, request, spider):
        if not request.cookies or not self.cookies_status:
            self.cookies_status = True
            cookies = self.ca.get_cookies()
            request.cookies == cookies
      
        return None
    def process_reponse(self, request, spider):
        if response.url.split("/")[2] == "verify.meituan.com":
            self.cookies_status = False





