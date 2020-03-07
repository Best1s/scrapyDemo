
import time, threading

cookies = None

lock = threading.Lock()
t = []
def test(th,i):
    time.sleep(3)
    global cookies
    if i%3 == 0:
        lock.acquire()      
        #print("i'm is i  ",i,"thread is ",th)
        cookies = None
        i=i+1
        lock.release()

    if not cookies :
        lock.acquire()        
        cookies = 1
        print("i'm thread ",th,",i is",i)
        lock.release()
    else:
        print("i'm thread ",th,"cookies exist")
 
def run_thread(n):
    for i in range(1,5):
        test(n,i)

ts = [threading.Thread(target=run_thread, args=(i,)) for i in range(5)]

[t.start() for t in ts]
[t.join() for t in ts]






