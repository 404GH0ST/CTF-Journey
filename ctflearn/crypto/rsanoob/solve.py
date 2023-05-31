from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto import Random
import Crypto
import sys
import libnum

c=9327565722767258308650643213344542404592011161659991421       
e=1
n=245841236512478852752909734912575581815967630033049838269083

print("\n\nAnswer:")
print(f"\nCipher: {c}, N={n}\n")


val=libnum.nroot(c,e)
print(f"\nIf we assume e: {e}, we take the third root to get: {val}")
print("Next we convert this integer to bytes, and display as a string.")
print(f"\nDecipher: {long_to_bytes(val).decode()}")