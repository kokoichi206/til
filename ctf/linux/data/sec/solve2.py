from Crypto.Util.number import *
from Crypto.Random import *
from math import gcd
# from mod_sqrt import modular_sqrt
# from mod_sqrt_2 import square_root

e = 131074
n = 587926815910957928506680558951380405698765957736660571041732511939308424899531125274073420353104933723578377320050609109973567093301465914201779673281463229043539776071848986139657349676692718889679333084650490543298408820393827884588301690661795023628407437321580294262453190086595632660415087049509707898690300735866307908684649384093580089579066927072306239235691848372795522705863097316041992762430583002647242874432616919707048872023450089003861892443175057
c1 = 92883677608593259107779614675340187389627152895287502713709168556367680044547229499881430201334665342299031232736527233576918819872441595012586353493994687554993850861284698771856524058389658082754805340430113793873484033099148690745409478343585721548477862484321261504696340989152768048722100452380071775092776100545951118812510485258151625980480449364841902275382168289834835592610827304151460005023283820809211181376463308232832041617730995269229706500778999
c2 = 46236476834113109832988500718245623668321130659753618396968458085371710919173095425312826538494027621684566936459628333712619089451210986870323342712049966508077935506288610960911880157875515961210931283604254773154117519276154872411593688579702575956948337592659599321668773003355325067112181265438366718228446448254354388848428310614023369655106639341893255469632846938342940907002778575355566044700049191772800859575284398246115317686284789740336401764665472
cm = 357982930129036534232652210898740711702843117900101310390536835935714799577440705618646343456679847613022604725158389766496649223820165598357113877892553200702943562674928769780834623569501835458020870291541041964954580145140283927441757571859062193670500697241155641475887438532923910772758985332976303801843564388289302751743334888885607686066607804176327367188812325636165858751339661015759861175537925741744142766298156196248822715533235458083173713289585866

p = gcd(c1 + c2, n)
q = gcd(c1 - c2, n)
r = n // (p * q)

print(f"p: {p}")
print(f"q: {q}")
print(f"r: {r}")

phi = (p-1)*(q-1)*(r-1)
print(f"phi: {phi}")

print(f"gcd(e, phi): {gcd(e, phi)}")

assert 2 == gcd(e, phi)

# ================== ↓↓↓ Modular Square Method ↓↓↓ ==================
import random
import time

def square_root(n, p):
    result = []
    for _ in range(40):
        time.sleep(0.5)
        random.seed()

        n %= p
        if pow(n, (p - 1) >> 1, p) != 1:
            return -1
        q = p - 1
        m = 0
        while q & 1 == 0:
            q >>= 1
            m += 1
        z = random.randint(1, p - 1)
        while pow(z, (p - 1) >> 1, p) == 1:
            z = random.randint(1, p - 1)
        c = pow(z, q, p)
        t = pow(n, q, p)
        r = pow(n, (q + 1) >> 1, p)
        if t == 0:
            return 0
        m -= 2
        while t != 1:
            while pow(t, 2**m, p) == 1:
                c = c * c % p
                m -= 1
            r = r * c % p
            c = c * c % p
            t = t * c % p
            m -= 1
        result.append(r)

    return set(result)
# ================== ↑↑↑ Modular Square Method ↑↑↑ ==================

# ================== ↓↓↓ Decryption ↓↓↓ ==================
# https://github.com/p4-team/ctf/tree/master/2016-03-12-0ctf/rsa
e = e // gcd(e, phi)

c_mod_p = cm % p
c_mod_q = cm % q
c_mod_r = cm % r
# print("c_mod_p, c_mod_q, c_mod_r")
# print(c_mod_p, c_mod_q, c_mod_r)

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


def gauss(c0, c1, c2, n0, n1, n2):
    N = n0 * n1 * n2
    N0 = N // n0
    N1 = N // n1
    N2 = N // n2
    d0 = modinv(N0, n0)
    d1 = modinv(N1, n1)
    d2 = modinv(N2, n2)
    return (c0*N0*d0 + c1*N1*d1 + c2*N2*d2) % N

roots0 = modular_sqrt(c_mod_p, p)
roots1 = modular_sqrt(c_mod_q, q)
roots2 = modular_sqrt(c_mod_r, r)
print("roots0")
print(roots0)
print("roots1")
print(roots1)
print("roots2")
print(roots2)
print("roots0, roots1, roots2")
print(p, q, r)

roots0 = square_root(c_mod_p, p)
roots1 = square_root(c_mod_q, q)
roots2 = square_root(c_mod_r, r)
print("roots0")
print(roots0)
print("roots1")
print(roots1)
print("roots2")
print(roots2)

with open('m_bytes', 'wb') as f:
    for r0 in roots0:
        for r1 in roots1:
            for r2 in roots2:
                print("r0, r1, r2")
                print(r0, r1, r2)
                M = gauss(r0, r1, r2, p, q, r)
                f.write(long_to_bytes(M))

                print(long_to_bytes(M))

# ================== ↑↑↑ Decryption ↑↑↑ ==================


roots0 = square_root(c_mod_p, p)
roots1 = square_root(c_mod_q, q)
roots2 = square_root(c_mod_r, r)
print("roots0")
print(roots0)
print("roots1")
print(roots1)
print("roots2")
print(roots2)

with open('m_bytes', 'wb') as f:
    for r0 in roots0:
        for r1 in roots1:
            for r2 in roots2:
                print("r0, r1, r2")
                print(r0, r1, r2)
                M = gauss(r0, r1, r2, p, q, r)
                f.write(long_to_bytes(M))
                print(long_to_bytes(M))


M = gauss(roots0, roots1, roots2, p, q, r)
print(long_to_bytes(M))
m_bytes = long_to_bytes(M)

# print(m_bytes.decode(""))

# with open('m_bytes', 'wb') as f:
#     f.write(m_bytes)


# m = pow(cm, d, n)

# print(f"m: {m}")

# m_bytes = long_to_bytes(m)
# print(f"m_bytes: {m_bytes}")

# with open('m_str', 'wb') as f:
#     f.write(m_bytes)



