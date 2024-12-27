from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes
from hashlib import sha256
import random

p = 0xdd6cc28d
g = 0x83e21c05

A = 0xcfabb6dd
B = 0xc4a21ba9


