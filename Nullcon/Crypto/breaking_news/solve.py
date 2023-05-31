from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

key1 = RSA.import_key(open('key1.private','rb').read()) # Got from wieners attack 
key2 = RSA.import_key(open('key2.pem','rb').read())

print(f"{key1.e=},{key1.n=}")
print(f"{key2.e=},{key2.n=}")

ciphers = open('ciphers','r').readlines()
ct1 = bytes.fromhex(ciphers[0].strip())
ct2 = bytes.fromhex(ciphers[1])

# msg 1
cryptor = PKCS1_OAEP.new(key1)
m1 = cryptor.decrypt(ct1)
print(m1)

# msg 2
q = key1.q
p = key1.p
assert p * q == key1.n # Because both of the keys have the same n value, it's easy to recover the private for key2

d2 = pow(key2.e, -1, (p - 1) * (q - 1)) # inverse(e, thotient)
key2 = RSA.construct((key2.n, key2.e, d2))
cryptor = PKCS1_OAEP.new(key2)
m2 = cryptor.decrypt(ct2)
print(m2)

print(f"Flag : {m1+m2}")