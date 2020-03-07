import twisted
import twisted.internet.defer
import twisted.internet.reactor
import time

class DeferHandle(object):
    def __init__(self):
        self.defer = twisted.internet.defer.Deferred()
    def get_defer(self):
        return self.defer
    def work(self):
        print("等待数据操作3s")
        time.sleep(3)
        self.defer.callback("finish") #执行回调

    def handle_success(self,result):   # 成功回调
        print("完成！接收到数据",result)
    def handle_error(self,exp): #错误回调
        print("error!",exp)

def main():
    defer_client = DeferHandle()  # 获取当前的回调操作
    twisted.internet.reactor.callWhenRunning(defer_client.work) # 运行模拟操作
    defer_client.get_defer().addCallback(defer_client.handle_success) # 执行完毕的回调
    defer_client.get_defer().addErrback(defer_client.handle_error)  # 错误的回调
    twisted.internet.reactor.callLater(5,stop)  # 5s 后停止Reactor的调用
    twisted.internet.reactor.run()
def stop():
    twisted.internet.reactor.stop()
    print("服务调用结束")

if __name__ == "__main__":
    main()