import demo.uapool as ua
import random
from twisted.internet.error import TimeoutError
class UaDownloaderMiddleware(object):
    
    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(ua.USER_AGENTS)

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            return request