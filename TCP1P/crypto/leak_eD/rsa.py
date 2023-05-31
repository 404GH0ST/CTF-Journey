#!/usr/bin/python3

from Crypto.Util.number import *

p = getPrime(1024)
q = getPrime(1024)
e = 5
n = p * q
phi = (p - 1) * (q - 1)
d = inverse(e,phi)
dl = d % (p - 1)

m = bytes_to_long(b'REDACTED')
c = pow(m, e, n)

print(f'n = {n}')
print(f'e = {e}')
print(f'c = {c}')
print(f'leakeD = {dl}')




