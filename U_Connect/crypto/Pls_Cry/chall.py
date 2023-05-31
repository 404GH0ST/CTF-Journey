from Crypto.Util.number import getPrime
from secret import flag

def encrypt(plaintext):
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    with open('cipher','wb') as f:
        for i in plaintext:
            c = (p * i + q) % n
            f.write(c.to_bytes(c.bit_length(),'little'))
        f.write(n.to_bytes(c.bit_length(),'little'))
        f.close()

cipher = encrypt(flag)

print('DONE!')