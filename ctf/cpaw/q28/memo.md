```sh
apt install scapy

scapy
```

```sh
scapy
# scapy の中でのこと
>>> packets = rdpcap('network100_be557d01b0299a03dd3569893226dda424efc9a0.pcap')
>>> len(packets)
95
>>> packets[1]
<Ether...
>>> packets[1]['IP']
<IP  ver...
>>> print(packets[1]['IP'].version)
4
>>> print(packets[1]['IP'].proto)
17
>>> print(packets[1]['IP'].ttl)
64
>>> print(packets[1]['IP'].src)
192.168.91.138
>>> print(packets[1]['IP'].dst)
192.168.91.2
>>> for p in packets:
...:     print(p['IP'].src)
...:
192.168.91.138
192.168.91.138
192.168.91.2
```

```
$ ftp

ftp> open

Remote system type is UNIX.
Using binary mode to transfer files.
ftp> passive
Passive mode: on; fallback to active mode: on.
ftp> passive
Passive mode: off; fallback to active mode: off.
ftp> passive
Passive mode: on; fallback to active mode: on.

ftp> get dummy
local: dummy remote: dummy
227 Entering Passive Mode (118,27,110,77,234,108).
150 Opening BINARY mode data connection for dummy (36 bytes).
100% |***********************|    36       12.74 KiB/s    00:00 ETA
226 Transfer complete.
36 bytes received in 00:00 (2.62 KiB/s)
```
