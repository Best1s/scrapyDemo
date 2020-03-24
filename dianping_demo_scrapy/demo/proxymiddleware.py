from demo.proxymodel import Proxy
from twisted.internet.defer import DeferredLock
class ProxyMiddleWare(object):
    def __init__(self):
        self.p = Proxy()
        self.proxy_status = True
        self.lock = DeferredLock()
        self.try_count = 2
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
    def process_response(self, request, response, spider):
        
        if response.status == 403 or "meituan" in response.url or response.status == 302:            
            self.lock.acquire()
            del request.meta["proxy"]
            self.proxy_status = True
            self.lock.release()
            self.try_count -= 1
            return request
        elif self.try_count == 0 :
             self.try_count = 2
        return response



