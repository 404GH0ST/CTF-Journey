#!/usr/bin/python
import binascii

FLAG = 'REDACTED'
KEY = # DELETED

def encrypt(plaintext):
    enc = []
    for s in plaintext:
        enc.append(ord(s) ^ key)
    return bytes(enc)

with open('encrypted.txt', 'wb') as f:
    f.write(b'FLAG: ' + binascii.hexlify(encrypt(FLAG)))