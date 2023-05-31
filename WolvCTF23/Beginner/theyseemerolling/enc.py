
from Crypto.Util.strxor import strxor
from Crypto.Util.number import long_to_bytes
import os

# key = os.urandom(8)
# print(key)
key = b'\x93\xe0T\xbeNtV\xce'
def encrypt_block(block):
  global key
  return strxor(key, block)

def encrypt(pt):
  ct = b''
  for i in range(0, len(pt), 4):
    index = long_to_bytes(i // 4)
    print("index variable value1:", index)
    index = b'\x00' * (4 - len(index)) + index
    print("index variable value2:", index)
    ct += encrypt_block(index + pt[i:i+4])
  return ct

if __name__ == '__main__':
  flag = open('flag', 'rb').read()
  flag += b'\x00' * (4 - len(flag) % 4)

  print(encrypt(flag).hex())

  
  print(encrypt(bytes.fromhex('93e054be391722a893e054bf351237a593e054bc2b2b30a293e054bd2f132bc493e054ba4e7456ce')))
