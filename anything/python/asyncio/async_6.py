import asyncio

loop = asyncio.get_event_loop()


async def main():
    print('start')
    print('done')


# loop.run(main())    # newer than 3.7
loop.run_until_complete(main())
loop.close()
