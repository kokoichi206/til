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

def f(num, arr):
    logging.debug(num)  # Synchronized wrapper for c_float(0.0)
    num.value += 1.0
    logging.debug(arr)
    for i in range(len(arr)):
        arr[i] *= 2

if __name__ == '__main__':
    # 共有メモリに値を作る。プロセスセーフにするための特別なもの
    num = multiprocessing.Value('f', 0.0)
    arr = multiprocessing.Array('i', [1, 2, 3, 4, 5])

    p = multiprocessing.Process(target=f, args=(num, arr))
    p.start()
    p.join()
    logging.debug(num.value)
    logging.debug(arr[:])
