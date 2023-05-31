
from Crypto.Util.strxor import strxor
from Crypto.Util.number import long_to_bytes
import os

def encrypt_block(block):
  global key
  return strxor(key, block)

def encrypt(pt):
  ct = b''
  for i in range(0, len(pt), 4):
    index = long_to_bytes(i // 4)
    index = b'\x00' * (4 - len(index)) + index
    ct += encrypt_block(index + pt[i:i+4])
  return ct

if __name__ == '__main__':
#   flag = open('flag', 'rb').read()
#   flag += b'\x00' * (4 - len(flag) % 4)

  for i in range(2**64):
        key = i.to_bytes(8, byteorder='big')
        pt = encrypt(bytes.fromhex('983f687f03f884a9983f687e0ff2afbc983f687d03a891bd983f687c2bf68990983f687b04e9c0a9983f687a2be8c4a6983f687910c482ff983f687818f7afb6983f687744ee8290983f687644ec9e90983f687517e989bf983f687400ab8dcf'))
        if b'wctf' in pt:
            print(pt)
            break
