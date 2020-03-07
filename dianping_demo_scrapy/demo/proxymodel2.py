import requests
import demo.uapool as ua
import random
import time

class Proxy(object):
    def __init__(self):
        self.url = "https://www.freeip.top/api/proxy_ip"
        #self.headers = {'Authorization': 'Basic cHJveHk6cHJveHkxMjMh'}
        #self.lock = DeferredLock()
    def get_proxy(self):
        #self.lock.acquire()        
        while True:
            try:
                ipinfo = requests.get(self.url).json()['data']
                ip = ipinfo['protocol'] + "://" + ipinfo['ip'] + ':' + ipinfo['port']
                print(ip)
                r = requests.get("http://www.dianping.com/shop/21134863",headers={"User-Agent":random.choice(ua.USER_AGENTS)}, proxies={ipinfo['protocol']:ip}, timeout=3)
                time.sleep(0.5)
            #except requests.exceptions.ConnectionError :
            #    self.delete_proxy(proxy=ip)
            except Exception as e:
                print(e)
                continue
            else:                
                if r.status_code == 200:
                    break
                    #self.lock.release()
        #print("proxy ip is : http://" + ip)                    
        return ip


