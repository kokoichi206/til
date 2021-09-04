from multiprocessing import (
    Process,
    Lock, RLock, Semaphore, Queue, Event, Condition, Barrier,
    Value, Array, Pipe, Manager
)

import logging
import multiprocessing
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='%(processName)s: %(message)s'
)

def worker1(i):
    logging.debug('start')
    time.sleep(3)
    logging.debug('end')
    return i + 1

if __name__ == '__main__':

    with multiprocessing.Pool(5) as p:
        r = p.map_async(worker1, [100, 200])  # リストの数分、実行？、get まで待つイメージ
        logging.debug('executed')
        logging.debug(r.get(timeout=1))
        # r = p.map(worker1, [100, 200])  # リストの数分、実行？、get まで待つイメージ
        # logging.debug('executed')
        # logging.debug(r)
        

    # with multiprocessing.Pool(5) as p:
    #     logging.debug(p.apply(worker1, (200, )))    # 同期ですすむ
    #     logging.debug('executed')
    #     p1 = p.apply_async(worker1, (100, ))
    #     p2 = p.apply_async(worker1, (100, ))
    #     logging.debug('executed')
    #     # logging.debug(p1.get(timeout=1))
    #     logging.debug(p1.get())
    #     logging.debug(p2.get())

    # # この時の挙動注意
    # with multiprocessing.Pool(1) as p:
    #     p1 = p.apply_async(worker1, (100, ))
    #     p2 = p.apply_async(worker1, (100, ))
    #     logging.debug('executed')
    #     logging.debug(p1.get())
    #     logging.debug(p2.get())

