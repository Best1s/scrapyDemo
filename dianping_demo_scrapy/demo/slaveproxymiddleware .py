from demo.proxymodel import Proxy
from twisted.internet.defer import DeferredLock
import demo.settings as settings
from redis import StrictRedis, ConnectionPool
import time
from twisted.internet.error import TimeoutError
class ProxyMiddleWare(object):
    def __init__(self):
        self.p = Proxy()
        self.proxy_status = True
        self.lock = DeferredLock()
        self.try_count = 3
        host = settings.REDIS_HOST
        port = settings.REDIS_PORT
        password = settings.REDIS_PASSWORD
        self.pool = ConnectionPool(host=host, port=port,  password=password)
        self.redis = StrictRedis(connection_pool=self.pool)
    def process_request(self, request, spider):

        if "porxy" not in request.meta and self.proxy_status:             
            self.lock.acquire()
            self.proxy_status=False
            proxy = self.p.get_proxy(spider)
            request.meta["proxy"] = proxy
            self.lock.release()

    def process_response(self, request, response, spider):        
        if response.status in [403,302,301]:
            self.lock.acquire()
            try:
                del request.meta["proxy"]
            except:
                pass
            self.proxy_status = True
            time.sleep(3)
            self.lock.release()
            self.try_count -= 1
            if self.try_count == 0:
                self.try_count = 3
                self.redis.lpush("dianping:start_urls",response.url)
                return response
            return request
        return response
    def process_exception(self, request, exception, spider):
        if isinstance(exception,TimeoutError):
            return request


