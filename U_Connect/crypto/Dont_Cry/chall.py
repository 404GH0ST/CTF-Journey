from Crypto.Util.number import *
from secret import flag

e = 7
n = getPrime(1024) * getPrime(1024)
c = pow(int(flag.hex(), 0x16) << (300 - len(flag)),e,n)

print("n : {}".format(n))
print("e : {}".format(e))
print("c : {}".format(c))
