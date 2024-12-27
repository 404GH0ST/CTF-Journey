from pwn import xor

flag_enc = open("./enc.txt", "rb").read().strip()

print(xor(b"\x22\x11\x75\xe1\x66\x12\x0a\x75\xe1\x66", flag_enc))
