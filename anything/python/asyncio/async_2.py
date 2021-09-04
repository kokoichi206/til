import asyncio
import multiprocessing
import threading
import time


loop = asyncio.get_event_loop()


# @asyncio.coroutine
# def worker():
    # print('start')
    # # time.sleep(2)     # 非同期として sleep できない！
    # yield from asyncio.sleep(2)
    # print('stop')

# native コルーチン
async def worker():
    print('start')
    await asyncio.sleep(2)
    print('stop')

if __name__ == '__main__':
    # loop.run_until_complete(asyncio.wait([worker(), worker()]))
    loop.run_until_complete(asyncio.wait([worker() for _ in range(100)]))
    loop.close()

    # シングルスレッド
    # worker()

    # マルチスレッド
    # t1 = threading.Thread(target=worker)
    # t2 = threading.Thread(target=worker)
    # t1.start()
    # t2.start()

    # マルチプロセス
    # t1 = multiprocessing.Process(target=worker)
    # t2 = multiprocessing.Process(target=worker)
    # t1.start()
    # t2.start()

