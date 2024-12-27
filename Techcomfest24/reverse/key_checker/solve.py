from pwn import xor, p64

flag_enc = [0x5a15715955270e75, 0x39727e370854130a, 0x4f721d155539727e, 0x5c552d5857311246]
known_flag = b"TCF2024"

flag_enc_bytes = [p64(i) for i in flag_enc]
print(flag_enc_bytes)
key = xor(flag_enc_bytes, known_flag)[:7]
print(key)

print(xor(flag_enc_bytes[-2], key))