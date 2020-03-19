from demo.proxymodel import Proxy
from twisted.internet.defer import DeferredLock
class ProxyMiddleWare(object):
    def __init__(self):
        self.p = Proxy()
        self.proxy_status = True
        self.lock = DeferredLock()
    def process_request(self, request, spider):

        if request.url.split('/')[3] == 'shop':
            request.cookies = {}

        if request.url.split('/')[3] == 'shop' and self.proxy_status:             
            self.lock.acquire()
            self.proxy_status=False
            proxy = self.p.get_proxy()
            request.meta["proxy"] = proxy
            self.lock.release()
        #elif "proxy" in request.meta:
        #    self.proxy_status = True
        #    del request.meta["proxy"]
    def process_reponse(self, request, response, spider):
        try_count = 2
        if response.status == 403 or "meituan" in response.url or response.status == 302:            
            self.lock.acquire()
            print("this is 403 status!!"*5)
            del request.meta["proxy"]
            self.proxy_status = True
            self.lock.release()
            try_count -= 1
            return request
        elif try_count == 0 :
             try_count = 2
        return response



