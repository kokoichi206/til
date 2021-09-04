import asyncio
import asyncio.subprocess
import sys


async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(stdout.decode())
    exitcode = await proc.wait()
    print(exitcode)

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.wait([
    run('ls -al'), run('date')
]))
loop.close()
