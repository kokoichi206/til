c1 = (p-q)^e mod n (= pqr)
c1 = p^e - q*p^(e-1) + ... - q^(e-1)*p + q^e (n = p*q *r)
↓
c1 = p^e - q*p^(e-1) + ... - q^(e-1)*p + q^e (n' = p*q)
= p^e + q^e (n' = p*q)
p = 2
q = 3
r = 5
N = pqr = 30
c1 = 140 = 20 (mod 30)
c1 = 20 (n' = 2\*3 = 6)

p = gcd(c1 + c2, n)
q = gcd(c1 - c2, n)

```sh
strings quiz | grep ctf4b

echo -en '\x00' | hexdump -C
00000000  00
           |.|
00000001
```

```python
from pwn import *

s = remote("find-flag.seccon.games", 10042)
s.shutdown("send")
print(s.recvall().decode())
```

## /proc/$pid/environ

プロセス ID からプロセスの環境変数を得る！

/proc/pid/environ で見ることができるのは、プロセスの初期環境？

```sh
$ strings /proc/$$/environ
USER=ubuntu
SSH_CLIENT=192.168.0.7 53009 22
XDG_SESSION_TYPE=tty
...
```

> For similar reasons, by default qs will only parse up to 1000 parameters.
