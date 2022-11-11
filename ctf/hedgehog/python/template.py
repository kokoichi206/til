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

s = connect('127.0.0.1', 4000)

# Write code here

interact(s)
