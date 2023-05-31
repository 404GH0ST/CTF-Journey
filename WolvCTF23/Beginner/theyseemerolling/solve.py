from Crypto.Util.strxor import strxor
from Crypto.Util.number import long_to_bytes

def decrypt_block(block, key):
  return strxor(key, block)

def decrypt(ct):
  pt = b''
  for i in range(0, len(ct), 4):
    index = long_to_bytes(i // 4)
    index = b'\x00' * (4 - len(index)) + index
    pt += decrypt_block(index + pt[i:i+4])
  return pt

if __name__ == '__main__':
    for key in range()
