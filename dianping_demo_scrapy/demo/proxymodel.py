import requests
import demo.user_agent as ua
import random
import time

class Proxy(object):
    def __init__(self):
        self.url = "http://47.106.254.210/"
        self.headers = {'Authorization': 'Basic cHJveHk6cHJveHkxMjMh'}
        #self.lock = DeferredLock()

    def delete_proxy(self,proxy):
        requests.get(self.url + "delete/?proxy={}".format(proxy), headers = self.headers)
        print("delete proxy ip success")

    def get_proxy(self):
        #self.lock.acquire()        
        while True:
            try:
                ip = requests.get(self.url + "get/", headers = self.headers).json().get("proxy")
                r = requests.get("http://www.dianping.com",headers={"User-Agent":random.choice(ua.USER_AGENTS)}, proxies={"http":"http://" + ip}, timeout=3)
                time.sleep(0.5)
            #except requests.exceptions.ConnectionError :
            #    self.delete_proxy(proxy=ip)
            except Exception as e:
                self.delete_proxy(proxy=ip)
            else:
                print("status is :" ,r.status_code)
                if r.status_code == 200:
                    break
                    #self.lock.release()                    
        return "http://" + ip


