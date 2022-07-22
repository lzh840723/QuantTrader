"""
    多线程
    如果你想同时请求发送多个请求，获取多个交易所的ticker数据如何处理？

"""
from threading import Thread, Lock
# import threading

# def print_hello(a, b, c):
#     print(a)
#     print(b)
#     print(c)
#
# t1 = Thread(target=print_hello, args=(1, 2, 3))  # kwargs={"a": 1,  "c": 3, "b": 2}
# t1.start()



# demo1
# import threading, time
# def run(num):
#     print("子线程%s开始..."%(threading.current_thread().name))
#     time.sleep(2)
#     print(num)
#     time.sleep(2)
#     # current_thread  返回一个当前线程的实例
#     print("子线程%s结束..."%(threading.current_thread().name))
# if __name__ == '__main__':
#     print("主线程%s启动..."%(threading.current_thread().name))
#     # 创建子线程
#     t = threading.Thread(target=run,args =(1,))
#     t.start()
#     t.join()
#
#     print("主线程%s结束..."%(threading.current_thread().name))


#多线程共享资源
# import threading
# from threading import Lock
# lock = Lock() # threading.Lock()
# num = 0
#
# def run(n):
#     global num
#     for i in range(1000000):
#         # print(n)
#         # num += n
#         # num -= n
#         # with open("file"):
#         #     pass
#
#         with lock:
#             num += n
#             num -= n
#
#         # lock.acquire()
#         # num = num - n
#         # num = num + n
#         # lock.release()
#
#
# if __name__ == '__main__':
#
#     t1 = threading.Thread(target=run,args=(6,))
#     t2 = threading.Thread(target=run,args=(9,))
#     t3 = threading.Thread(target=run,args=(5,))
#     t3.start()
#     t1.start()
#     t2.start()
#     t1.join()
#     t2.join()
#     t3.join()
#     print("num = %s"%(num))
#
#
#
import time

class MyThread(Thread):
    def __init__(self, exchange):
        # super(MyThread, self).__init__()
        super(MyThread, self).__init__()
        self.name = "hello world"
        self.exchange = exchange

    def run(self):
        while True:
            print(f"request {self.exchange} BTCUSDT.....")
            time.sleep(2)



if __name__ == '__main__':
    thread = MyThread("Huobi")
    thread.start()

    thread_binance = MyThread("币安")
    thread_binance.start()

