import os, sys

ret = os.fork()

if ret == 0:
    # child process
    print(f"child: pid=%{os.getpid()}, parent pid={os.getppid()}")
    os.execve("/bin/echo", ["/bin/echo", f"hello from child process {os.getpid()}"], {})
elif ret > 0:
    # parent process
    # got child process pid as return value
    print(f"parent: pid={os.getpid()}, child: pid={ret}")
    os.execve("/bin/echo", ["/bin/echo", f"hello from parent process {os.getpid()}"], {})

sys.exit(0)
