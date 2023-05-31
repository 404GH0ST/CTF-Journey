#!/usr/bin/env python3

from Crypto.Util.number import *
from base64 import b64encode
from random import choice, shuffle

def get_private_key():
	pk_dict = [getPrime(512) for _ in range(500)] * 100
	shuffle(pk_dict)

	p, q = choice(pk_dict), choice(pk_dict)
	while p == q:
		p, q = choice(pk_dict), choice(pk_dict)

	with open('dicc.txt', 'w') as w:
		for pq in pk_dict:
			w.write(str(pq) + '\n')
	return [p, q]

flag = 'uconnect{RSA_Fake_flag_dek_xixixixi}'
c = bytes_to_long(flag.encode())
p, q = get_private_key()
n = p * q
e = 0x10001
enc = pow(c, e, n)
cipher = b64encode(long_to_bytes(enc)).decode()

with open('flag.enc', 'w') as w:
	w.write(cipher)
