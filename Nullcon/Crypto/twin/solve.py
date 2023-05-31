from sage.all import xgcd,Integer
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes

key1 = RSA.import_key(open('key1.pem','rb').read())
key2 = RSA.import_key(open('key2.pem','rb').read())
cipher = open('ciphers','r').readlines()

c1 = int(cipher[0])
c2 = int(cipher[1])
n = key1.n # It doesn't matter which key, because the value is same
 
d, u, v = xgcd(key1.e, key2.e)

m = pow(c1, u, n) * pow(c2, v, n)

m = Integer(m).nth_root(d)

print("Common Modulus Attack Variant {m^GCD(e1,e2), where GCD(e1,e2) = 17, it can be nth-rooted}")
print("Flag:",long_to_bytes(m).decode('utf-8'))

