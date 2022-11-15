from Crypto.Util.number import *
from Crypto.Random import *
# from flag import flag

flag = b"0830fef177c3e5dcffe2e1e5475326b45ee1a7f1"
flag = b"SECCON{hogehoge}"

# 512 桁の素数。。。
# getPrime(N:int, randfunc:callable):long Return a random N-bit prime number.
p = getPrime(512)
q = getPrime(512)
r = getPrime(512)

# solve で解いた値
p = 7572427786695057270624844967644562609112132599800420296747189080920032359205995588384031542287784540006438555802994008688795974493684400576592403320929717
q = 8609258896430210586523688955272794335561428099377427081622836355194006054569349679983850344916908011330202034512905353365631416251631307084038768336538857
r = 9018251874561850467651399512661829039310834429345808807288228370045576292997274498659156953954383290793552486677903139680704353709352146165598701061994853

n = p * q * r
# print(p)
# print(q)
# print(r)
# print(n)
# Fermat number F4
# 65537 = 2^2^4 + 1
e = 2 * 65537


assert n.bit_length() // 8 - len(flag) > 0
padding = get_random_bytes(n.bit_length() // 8 - len(flag))
print(type(padding))
m = bytes_to_long(padding + flag)

assert m < n

c1p = pow(p, e, n)
c1q = pow(q, e, n)
cm = pow(m, e, n)

c1 = (c1p - c1q) % n
c2 = pow(p - q, e, n)

# 今回のヒント
# p^e - q^e mod n
print(f"c1 = {c1}")
# (p-q)^e mod n (= pqr)
# p^e - q*p^(e-1) + ... - q^(e-1)*p + q^e (n = p*q)
# = p^e + q^e (n = p*q)
print(f"c2 = {c2}")



# n,e は通常公開されてるもの（公開鍵）
print(f"e = {e}")
print(f"n = {n}")


# 暗号文
# m^e mod n
print(f"cm = {cm}")





# print(p)
# print(q)
# print(r)
# print(n)
# print(type(p))
# print(cm)

# with open('test', 'wb') as f:
#     f.write(long_to_bytes(cm))


# print(long_to_bytes(cm))
# print(str(long_to_bytes(cm), 'CP932'))
# print(long_to_bytes(cm).decode('utf-8'))

