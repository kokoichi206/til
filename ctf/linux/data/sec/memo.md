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
c1 = 20 (n' = 2*3 = 6)

p = gcd(c1 + c2, n)
q = gcd(c1 - c2, n)

