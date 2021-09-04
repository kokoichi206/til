import logging
import queue
import threading
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='%(threadName)s: %(message)s'
)

def worker1(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(5)
        logging.debug('end')
    #     i = d['x']
    #     time.sleep(5)
    #     d['x'] = i + 1
    #     logging.debug(d)
    #     with semaphore:
    #         d['x'] = i + 1
    # logging.debug('end')

# def worker2(d, semaphore):
#     logging.debug('start')
#     semaphore.acquire()
#     i = d['x']
#     d['x'] = i + 1
#     logging.debug(d)
#     semaphore.release()
#     logging.debug('end')

def worker2(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(5)
        logging.debug('end')

def worker3(semaphore):
    with semaphore:
        logging.debug('start')
        time.sleep(5)
        logging.debug('end')

if __name__ == '__main__':

    d = {'x': 0}
    # semaphore = threading.Lock()
    semaphore = threading.Semaphore(2)
    t1 = threading.Thread(target=worker1, args=(semaphore, ))
    t2 = threading.Thread(target=worker2, args=(semaphore, ))
    t3 = threading.Thread(target=worker3, args=(semaphore, ))
    t1.start()
    t2.start()
    t3.start()

    # d = {'x': 0}
    # # lock = threading.Lock()
    # lock = threading.RLock()
    # t1 = threading.Thread(target=worker1, args=(d, lock))
    # t2 = threading.Thread(target=worker2, args=(d, lock))
    # t1.start()
    # t2.start()


    # t = threading.Timer(3, worker1)
    # t.start()

    # t1 = threading.Thread(name="rename worker1", target=worker1)
    # t2 = threading.Thread(target=worker2, args=(100, ), kwargs={'y': 200})
    
    # threads = []
    # for _ in range(5):
    #     t = threading.Thread(target=worker1)
    #     t.setDaemon(True)
    #     t.start()
    #     # threads.append(t)
    # print(threading.enumerate())
    # for thread in threading.enumerate():
    #     if thread is threading.currentThread():
    #         print(thread)
    #         continue
    #     thread.join()

    # t1 = threading.Thread(target=worker1)
    # t1.setDaemon(True)  # ほっておいて終了させる
    # t2 = threading.Thread(target=worker2)
    # t1.start()
    # t2.start()
    # print('started')
    # t1.join()   # やっぱり、デーモン化されたものでも待つ。
    # t2.join()
