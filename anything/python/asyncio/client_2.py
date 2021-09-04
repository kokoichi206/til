import asyncio


class AwaitableClass(object):
    def __init__(self, name, loop):
        self.name = name
        self.loop = loop
    
    def __await__(self):
        reader, writer = yield from asyncio.open_connection(
            '127.0.0.1', 8888, loop=self.loop
        )
        writer.write(self.name.encode())
        writer.write_eof()
        data = yield from reader.read()
        data = int(data.decode())
        return data
        

class AsyncIterater(object):
    def __init__(self, name, loop):
        self.name = name
        self.loop = loop
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        data = await AwaitableClass(self.name, self.loop)
        if data < 0:
            raise StopAsyncIteration
        return data

async def main(name, loop):
    print('chunc reader')
    result = await AwaitableClass(name, loop)
    print(result)
    # async for i in AsyncIterater(name, loop):
        # print(i)

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.wait([
    main('task1', loop), main('task2', loop)
]))
loop.close()
