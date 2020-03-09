from selenium import webdriver
import os
import time
import random

class SeleniumDownloaderMiddleware(object):
    def __init__(self):
        self.driver_path = os.getcwd() + "\chromedriver80.0.3987.16.exe"
        self.browser = webdriver.Chrome(self.driver_path)
        self.browser.implicitly_wait(10)  # 隐性等待，最长等10秒
        self.browser.set_window_size(700, 1000)        

    def process_request(self, request, spider):
        if requet.url == "https://z.jd.com/bigger/search.html":
            self.browser.get(request.url)
            
                 
        return None
    def process_reponse(self, request, spider):
        if response.url.split("/")[2] == "verify.meituan.com":
            self.cookies_status = False
        return response








