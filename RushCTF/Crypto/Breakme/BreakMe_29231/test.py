from Crypto.Util.number import *
from Crypto.PublicKey import RSA


FLAG = ""
with open("flag.txt", "rb") as f:
    FLAG = f.read()

p = getPrime(2048)
p_factor = p
print(p_factor)
p *= p
print(p)
q = pow(p_factor, 6)
print(q)
e = 0x10001
N = p*q

"""
-
-
-
VANISHED CODE 
(known information: the cipher is just a textbook rsa)
-
-
-
"""

phi = (p - 1) * (q - 1)

d = inverse(e, phi)
ciphertext = pow(FLAG, e, N)
exported = RSA.construct( ( N, e ) ).publickey().exportKey()

with open("test.pem", 'wb') as f:
    f.write(exported)

with open('test.txt', 'w') as f:
    f.write(ciphertext.hex())

