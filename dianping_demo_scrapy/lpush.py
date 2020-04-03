import demo.settings as settings
import MySQLdb
from redis import StrictRedis, ConnectionPool
import threading    
import time
#集合中未抓取到的url,重新抓取

class Push(threading.Thread):
    def __init__(self):
        rhost = settings.REDIS_HOST
        rport = settings.REDIS_PORT
        rpassword = settings.REDIS_PASSWORD
        pool = ConnectionPool(host=rhost, port=rport,  password=rpassword)
        redis = StrictRedis(connection_pool=pool)
        self.urls = list(redis.smembers("lpushed_shop_url"))
        print("urls number is",len(self.urls))
        redis.close()
        self.host = settings.DB_HOST
        self.user = settings.DB_USER
        self.password = settings.DB_PASSWORD
        self.database = settings.DB_DATABASE
        self.sum=0
        threading.Thread.__init__(self)
        self.lock = threading.Lock()

    def query_url(self, url):
        try:
            db = MySQLdb.connect(self.host, self.database, self.password, self.user, charset='utf8')
            cursor = db.cursor()
        except Exception as e:
            print("mysql connect [ERROR]:",e)
        sql = "select id from shop_info where shop_url = '%s' " % url.decode()
        result = cursor.execute(sql)
        db.close()
        return result

    def push_url(self, start ,end):        
        for i in range(start,end):                      
            #result = cursor.fetchone()
            if not self.query_url(self.urls[i]):
                self.lock.acquire()
                self.sum+=1
                self.lock.release()
                print("push url",self.urls[i])
                redis.lpush("dianping:start_urls",url)

    def main(self, t_num=5):
        urls_num = len(self.urls) // t_num
        ts = []
        for i in range(0,t_num):
            start = urls_num * i
            end = urls_num * (i+1)
            if i+1 == t_num:
                end = len(self.urls)-1
            t = threading.Thread(target=self.push_url, args=(start, end))
        ts.append(t)
        for t in ts:
            t.start()
        for i in ts:
            t.join()
        time.sleep(1)
        print("push url complete! num is:",self.sum)

if __name__ == "__main__":
    q = Push()
    q.main()
    