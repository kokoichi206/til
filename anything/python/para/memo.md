マルチスレッドとマルチプロセスのイメージ

デーモン化されてないものに関しては、join を書かなくても一緒
あえて明示的に join することもある

### Lock と RLock

with statement が便利

```python
def worker1(d, lock):
    logging.debug('start')
    with lock:
        i = d['x']
        time.sleep(5)
        d['x'] = i + 1
        logging.debug(d)
        with lock:
            d['x'] = i + 1
    logging.debug('end')
```

Lock in Lock を避けるために、RLock がある！

### セマフォ

Lock は同時に走れるスレッド数が必ず１だったが、セマフォはロックをかける数を制限できる

```python
threading.Semaphore(2)
```

### キュー
ワーカー間でのデータのやり取り？

queue.get は、値が入ってくるまで待つ！待ち続ける。

queue 自体がスレッドを管理する

```python
print(queue.get())

```

### イベント
`event.set` を待つためのものが、`event.wait()`

### コンディション
event と lock の組み合わせ、みたいな感じ

### マップ
iteratorを返したかったら、imap

multiprocessing.Process の時点で fork が走る

デュアルコアなど、ハードのメリットが活かせるならマルチプロセスかな

