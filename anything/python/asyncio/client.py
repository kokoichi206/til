import asyncio


async def request_server(name, loop):
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888, loop=loop
    )
    writer.write(name.encode())
    writer.write_eof()
    data = await reader.read()
    data = int(data.decode())
    return data

async def main(name, loop):
    print('chunc reader')
    result = await request_server(name, loop)
    print(result)

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.wait([
    main('task1', loop), main('task2', loop)
]))
loop.close()

# @asyncio.coroutine
# def tcp_echo_client(message, loop):
#     reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888,
#                                                         loop=loop)

#     print('Send: %r' % message)
#     writer.write(message.encode())

#     data = yield from reader.read(100)
#     print('Received: %r' % data.decode())

#     print('Close the socket')
#     writer.close()

# message = 'Hello World!'
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait([
#     tcp_echo_client(message, loop),
#     tcp_echo_client(message, loop),
#     tcp_echo_client(message, loop),
#     tcp_echo_client(message, loop)
# ]))
# loop.close()
