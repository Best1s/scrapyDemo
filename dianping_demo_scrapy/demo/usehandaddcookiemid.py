import random
from demo.cookiespool import COOKIES as ckpool
import time
class UseHandAddCookiesDownloaderMiddleware(object):
    def __init__(self):        
        self.cookies_status = False

    def get_cookies(self):
        cookies = random.choice(ckpool)
        cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}
        return cookies

    def process_request(self, request, spider):

        if not request.cookies or not self.cookies_status:
            self.cookies_status = True
            cookies = self.get_cookies()
            request.cookies = cookies
        return None

    def process_response(self, response,request, spider):

        if response.url.split("/")[2] == "verify.meituan.com" or response.status == 403:
            time.sleep(5)
            #print("this is 403!!!!"*3)
            #self.cookies_status = False
            #self.request.cookies = {}
            #self.crawler.engine.close_spider(self, 'url change is' + response.url + 'stop crawl!')
        return response




