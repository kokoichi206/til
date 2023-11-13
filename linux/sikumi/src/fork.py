import os, sys

ret = os.fork()

if ret == 0:
    # child process
    print(f"child: pid=%{os.getpid()}, parent pid={os.getppid()}")
    exit()
elif ret > 0:
    # parent process
    # got child process pid as return value
    print(f"parent: pid={os.getpid()}, child: pid={ret}")
    exit()

sys.exit(0)
