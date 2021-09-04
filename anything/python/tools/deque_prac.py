import collections
import queue

# Double-end queue
collections.deque

q = queue.Queue()
lq = queue.LifoQueue()
l = []
d = collections.deque()  # メモリ関係上、高速に取り出せる

for i in range(3):
    q.put(i)
    lq.put(i)
    l.append(i)
    d.append(i)

# for _ in range(3):
#     print('FIFO queue = {}'.format(q.get()))
#     print('LIFO queue = {}'.format(lq.get()))
#     print('list       = {}'.format(l.pop()))
#     print('deque      = {}'.format(d.pop())) # popleft
#     print()

# リストのようにも扱える
print(d[1])
print(d[-1])
print(d)
d.rotate()
print(d)
d.extendleft('x')
print(d)
d.extend('y')
print(d)
