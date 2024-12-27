from pwn import xor

flag_enc = open("./enc.txt", "rb").read().strip()

print(xor(b"\x76\x22\x99\xf2\x11\x67\xfe\x66", flag_enc))
