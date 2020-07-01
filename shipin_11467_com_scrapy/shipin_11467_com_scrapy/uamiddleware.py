import shipin_11467_com_scrapy.uapool as ua
import random

class UaDownloaderMiddleware(object):
    
    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(ua.USER_AGENTS)


