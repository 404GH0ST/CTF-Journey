from pwn import xor
from itertools import cycle

def x0r(val1, val2):
    return bytes(x ^ ord(y) for x,y in zip(val1, cycle(val2))).decode()

flag_enc = b'\t\x1b\x11\x00\x16\x0b\x1d\x19\x17\x0b\x05\x1d(\x05\x005\x1b\x1f\t,\r\x00\x18\x1c\x0e'

# print(xor(flag_enc, 'jowls')) # got from xor(flag_enc[:5], 'ctfle')

key = x0r(flag_enc[:5], 'ctfle')

flag = x0r(flag_enc, key)
print(flag)