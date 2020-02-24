from demo.proxymodel import Proxy
class ProxyMiddleWare(object):
    def __init__(self):
        self.p = Proxy()
        self.proxy_status = False
    def process_request(self, request, spider):
        if "proxy" not in request.meta or not self.proxy_status:
            #self.proxy_status = True
            proxy = self.p.get_proxy()
            print("获取到代理：",proxy)
            request.meta["proxy"] = proxy




